from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import *
from category.models import *
from carts.views import _cart_id
from carts.models import *
# Create your views here.

def store(request, category_slug=None):
    # these are flags which are used to see whether the fields are empty or not
    categories = None
    products = None
    
    # if there's a slug in the field, then the following code should run
    
    #     Use get() to return an object, or raise an Http404 exception if the object
    # does not exist.

    # klass may be a Model, Manager, or QuerySet object. All other passed
    # arguments and keyword arguments are used in the get() query.
    
    # Like with QuerySet.get(), MultipleObjectsReturned is raised if more than
    # one object is found.
    if category_slug != None:
        # here the database id queried and get the object based on the slug... the slug there refers to the slug field in the model Category,
        # while the category_slug is what the user requested for... so if it matches, then get the object else throw a 404 error.
        categories = get_object_or_404(Category, slug=category_slug)
        # Here it should filter the product that has been got in the up code, then, the category 
        products = Product.objects.filter(category=categories, is_available=True)
        paginator = Paginator(Paginator, 3)
        
        page = request.GET.get('page')
        paged_products = paginator.get_page(page) 
        product_count = products.count()
    else:
        # Just show all the total products 
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 3)
        
        page = request.GET.get('page')
        paged_products = paginator.get_page(page) 
        
        # the count method is used to count the total instances within a modelSS
        product_count = products.count()

    
    
    context = {
        'products' : paged_products,
        'product_count' : product_count,
    }
    return render(request, 'store/store.html', context)


# This view takes three positional argument, one for the request, one for the category and the other for a specific product
def product_detail(request, category_slug, product_slug):
    try:
        # Here, the product is retrieved from the data base and it is depicted as follows:
        # category__slug means in the product model, look for category field and since it hahs double underscore, it means, we are trying to access another field which makes it a foriegn key.
        # so in the Product model, look for the category field, and in the category field, go to Category model and look for slug and match it.
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        # checking to see if the cart item is not empty
        # Here, the cart being a foreign key, is accessed and then, it is filtered based on the session_key. If it matches...
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
        
        
    
    except Exception as e:
        raise e
    
    context = {
        'single_product' : single_product,
        'in_cart': in_cart
    }
    return render(request, 'store/product_detail.html', context)


def search(request):
    products = ''
    product_count = ''
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
    context = {
        'products': products,
        'product_count' : product_count
    }
    return render(request, 'store/store.html', context)