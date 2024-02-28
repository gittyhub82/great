from .models import *

from .views import _cart_id


def counter(request):
    # here checks if the user requests for an admin page, then it should only return an empty disctionary as the admin page doesn't need the counter
    cart_count = 0
    if 'admin' in request.path:
        return {}
    
    else:
        # Here if the result is false...
        # get the session key of the cart then assigned it to the cart variable,
        # then in the cart_item, we are gonna bring all the items that are in the cartitem based, but only those with session key
        try:
            # always try to remember that the session key comes with a request from the user, so it needs to accept a request
            
            #since the context processor count fucnction is the one that adds the number of a product in the cart image, now it is going to be based on the user
            
            cart = Cart.objects.filter(cart_id=_cart_id(request))
            # if the user is really authenticated, then assigns the counter to the user 
            if request.user.is_authenticated:
                cart_items = CartItem.objects.all().filter(user=request.user)    
            else:
                cart_items = CartItem.objects.all().filter(cart=cart[:1])
            
            # looping through the cartitem so that it can be printed indiidually and assigned to a key value 'links'
            for cart_item in cart_items:
                # remember, we are trying to increase the quantity of the product in the cart item
                cart_count += cart_item.quantity
                # print(cart_count)
        
        except Cart.DoesNotExist:
            cart_count = 0
        # after the data has been looped, it should return data in a dictionary format,
        # the key should be a'cart_count' together with what is inn the cart_item being the key
    return dict(cart_count=cart_count)