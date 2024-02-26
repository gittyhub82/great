from django.urls import path

from . import views

app_name = 'carts'

urlpatterns = [
    path('', views.cart, name='cart'),
    # the add_cart url is added so that the user's cart increased when he adds a cart
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),
    # This is the remove cart function which removes one particular product at a time
    path('remove_cart/<int:product_id>/<int:cart_item_id>/', views.remove_cart, name='remove_cart'),
    # This here removes everything from the cart
    path('remove_cart_item/<int:product_id>/<int:cart_item_id>/', views.remove_cart_item, name='remove_cart_item'),
    
]