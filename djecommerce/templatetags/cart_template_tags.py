from django import template
from djecommerce.models import Order

# register the template tag

register = template.Library()

@register.filter
def cart_item_count(user):
    # check if user is authenticated, and filter the order
    if user.is_authenticated:
        query_set = Order.objects.filter(user=user, ordered=False)
        if query_set.exists():
            return query_set[0].items.count()
    return 0
