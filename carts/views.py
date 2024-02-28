from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required


from store.models import Product, Variation
from carts.models import *
from django.http import HttpResponse

# Create your views here.

# first we have to get the cart_id from the session
# That session is  what we need when a user adds a product to cart. That 'session id' is actually important
def _cart_id(request):
    """
    Here, a session is actually checked tp see if the user that requests a thing has a session_key
    if it does, fine, no, then create a new session for the user and return it
    
    """
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id) #What this does is it retrives a specific product by it id. it checks whether it is there
    
    
    if current_user.is_authenticated:
        product_variation = []
        # Checks to see if the request submitted is a get or post
        if request.method == 'POST':
            # this here after the user submits the data, it comes to the backend which is assigned to the color and size variables
            # color = request.POST['color']
            # size = request.POST['size']
            # print(color, size)
            
            # the code above, shows that what it does it just that it gets the value submitted by the client; but there is a simpler method of doing this
            for item in request.POST:
                # here it iterates and assigns the 'key' to the request, to the key variable
                key = item
                # this here gets the value of the key and assigns it to the value variable
                value = request.POST[key]
                try:
                    # checking what the user submits matches the variation in our database together with the product
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    #since we can have many variations in the cartitem,  we append the items and store them in a list
                    product_variation.append(variation)
                    # print(product_variation)
                except Variation.DoesNotExist:
                    pass
                
        # try:
        #     cart = Cart.objects.get(cart_id=_cart_id(request))
            
        # except Cart.DoesNotExist:
        #     cart = Cart.objects.create(
        #         cart_id=_cart_id(request)
        #     )
        
        # cart.save()
        
        
        # first, we have to check if cartitem exists or not
        # since it is not grouping it in the cartitems, so let's do it now, but we have to make the try block into if-else statement
        
        
        # check if cart_item exists
        
        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        if is_cart_item_exists:
            # assigning the cart item to the current user
            cart_item = CartItem.objects.filter(product=product, user=current_user)
            
            
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)
                
            if product_variation in ex_var_list:
                # we are going to look for the id and increased it
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            
            else:
                item = CartItem.objects.create(product=product, quantity=1, user=current_user)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
                
                
        else:
            cart_item = CartItem.objects.create(product=product, quantity= 1, user=current_user)
            if len(product_variation) > 0 :
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('carts:cart')
            
    # return HttpResponse(cart_item.quantity)
    # exit() Here it checks for the quantity to see that the product is actually add to cart
    
    
    # end of the current user and the start of the anonymous user
    
    
    else:
        product_variation = []
    # Checks to see if the request submitted is a get or post
        if request.method == 'POST':
            # this here after the user submits the data, it comes to the backend which is assigned to the color and size variables
            # color = request.POST['color']
            # size = request.POST['size']
            # print(color, size)
            
            # the code above, shows that what it does it just that it gets the value submitted by the client; but there is a simpler method of doing this
            for item in request.POST:
                # here it iterates and assigns the 'key' to the request, to the key variable
                key = item
                # this here gets the value of the key and assigns it to the value variable
                value = request.POST[key]
                try:
                    # checking what the user submits matches the variation in our database together with the product
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    #since we can have many variations in the cartitem,  we append the items and store them in a list
                    product_variation.append(variation)
                    # print(product_variation)
                except Variation.DoesNotExist:
                    pass
                
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id=_cart_id(request)
            )
        
        cart.save()
        
        
        # first, we have to check if cartitem exists or not
        # since it is not grouping it in the cartitems, so let's do it now, but we have to make the try block into if-else statement
        
        
        # check if cart_item exists
        
        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, cart=cart)
            
            
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)
                
            if product_variation in ex_var_list:
                # we are going to look for the id and increased it
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            
            else:
                item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
                
                
        else:
            cart_item = CartItem.objects.create(product=product, quantity= 1, cart=cart)
            if len(product_variation) > 0 :
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('carts:cart')
            
# return HttpResponse(cart_item.quantity)
# exit() Here it checks for the quantity to see that the product is actually add to cart




# the cart_item_id is added so as to delete that very product, not just any product.
# fixing the remove button for when logged in user
def remove_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    
    
    try:
        # here the item is checked together with thw product, cart and the id of the cart_item_id
        # first we have to check to see whether user is authenticated
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            # here it should decrease the product based on the anonymous user.
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        
        if cart_item.quantity > 1 :
            cart_item.quantity -= 1
            cart_item.save()
        
        else:
            cart_item.delete()
    except:
        pass 
    
    return redirect('carts:cart')


def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    
    try:
        # samething for the remove all button
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(user=request.user, product=product, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(cart=cart, product=product, id=cart_item_id)
    except:
        pass
    
    cart_item.delete()
    return redirect('carts:cart')

def cart(request, total=0, quantity=0, cart_items=None):
    
    try:
        tax = 0
        grand_total = 0
        # same thing we did as in the counter
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:    
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total) / 100
        grand_total = total + tax
            
    except ObjectDoesNotExist as e:
        return render(request,'carts/cart.html')
    
    context = {
        'cart_items': cart_items,
        'total' : total,
        'quantity' : quantity,
        'tax' : tax,
        'grand_total' : grand_total,
    }
    return render(request, 'carts/cart.html', context)

# To actually checkout your products that you have saved in the cart; one needs to sign-in and move their product to the checkout
@login_required(login_url='accounts:login')
def checkout(request, total=0, quantity=0, cart_items=None):
    
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:    
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total) / 100
        grand_total = total + tax
            
    except ObjectDoesNotExist as e:
        return render(request,'carts/cart.html')
    
    context = {
        'cart_items': cart_items,
        'total' : total,
        'quantity' : quantity,
        'tax' : tax,
        'grand_total' : grand_total,
    }
    return render(request, 'carts/checkout.html', context)