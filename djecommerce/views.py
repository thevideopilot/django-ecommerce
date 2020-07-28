from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import Item, Order, OrderItem
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from django.shortcuts import redirect

# Create your views here.



class HomeView(ListView):
    model = Item
    paginate_by = 5
    template_name = "djecommerce/home.html"

# Make this inherit from a view instead of a DetailView
class OrderSummaryView(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'djecommerce/order_summary_detail.html')


def home(resquest):
    context = {
        'items': Item.objects.all()
    }
    return render(resquest, 'djecommerce/home.html', context)


def checkout(request):

    return render(request, 'djecommerce/checkout-page.html')



class ItemDetailtView(DetailView):
    model = Item
    template_name = "djecommerce/product-page.html"


def product(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, 'djecommerce/product-page.html', context)


# the get_or_create method helps to get or create on some conditions and returns a tuple
def add_to_cart(request, slug):
    # get the item
    item = get_object_or_404(Item, slug=slug)
    # create a new order item or get an existing order item
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    # check if there is an order for this user that is not ordered yet
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated")
            return redirect("djecommerce:product", slug=slug)


        else:
            messages.info(request, "This item was added to your cart")
            order.items.add(order_item)
            return redirect("djecommerce:product", slug=slug)

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart")
        return redirect("djecommerce:product", slug=slug)


def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)  # get item slug url
    # check if there is an order for this user that is not ordered yet
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    # if the query set exists, get the order i.e if the user has an order
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order i.e filter the order for that specific item slug
        # then grab the order_item and remove.
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request, "This item was removed from your cart")
            return redirect("djecommerce:product", slug=slug)
        else:
            # add a message saying the order does not contain the order item.
            messages.info(request, "This item was not in your cart")
            return redirect("djecommerce:product", slug=slug)
    else:
        # add a message saying the user doesn't have an order
        messages.info(request, "You do not have an active order")
        return redirect("djecommerce:product", slug=slug)
