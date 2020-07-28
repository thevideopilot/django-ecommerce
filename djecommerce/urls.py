from django.urls import path
from .views import (
    home,
    checkout,
    product,
    HomeView,
    ItemDetailtView,
    OrderSummaryView,
    add_to_cart,
    remove_from_cart
)

app_name = 'djecommerce'

urlpatterns = [
    path('', HomeView.as_view(), name='home_ecom'),
    path('checkout/', checkout, name='checkout'),
    path('product/<slug>/', ItemDetailtView.as_view(), name='product'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart')

]
