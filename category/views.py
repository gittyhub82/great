from django.shortcuts import render



from store.models import *
# Create your views here.


def index(request):
    """
        this is going to render all the products in the database
    """
    # the all() gets everything in the database for you
    # the filter() is like a sieve that helps you sift through your db and get only the data you re interested in
    # Here, the products will show based on if they are available. That's what the filter method does
    products = Product.objects.all().filter(is_available=True)
    
    context = {
        'products': products,
    }
    return render(request, 'category/index.html', context)