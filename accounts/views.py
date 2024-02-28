from django.shortcuts import render, redirect
from .forms import *

from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from .models import *
from carts.models import *
from store.views import _cart_id
# Create your views here.


# these are the imports you need to make for you to use the the token  to activate a user accounts
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

import requests



def register(request):
    if request.method == 'POST':
        # this code executes when data is actually sent in a post request
        form = RegistrationForm(request.POST)
        # here i am getting the data being submitted by the new user, getting they word...
        # always remember, your form has to be valid before it is submitted, check always
        
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            # this here get the email and splits it in to two, taking the first index
            username = email.split("@")[0]
            
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            # since we not using the phone_number as a means for validation, we can tie it manually
            user.phone_number = phone_number
            user.save()
            # this is where email is sent to the user to activate their accounts; many imports are needed for this...
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain' : current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            
            to_mail = email
            send_email = EmailMessage(mail_subject, message, to=[to_mail])
            send_email.send()
            # messages.success(request, 'Registration Successful. Check spam')
            # this code here gets the email and the command from the browser which will tell the user to actually activate their account
            return redirect('/accounts/login/?command=verification&email='+email)
            
            
            # after registration has been successful, show the 'Registration Successful to the user 'alert' '
            # messages.success(request, 'Registration Successful.')
            # return redirect('accounts:register')

    else:
         form = RegistrationForm()
        
    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)


def login(request):
    # here is the code for when a user logs in
    if request.method == 'POST':
        # get the email and password submitted by the user
        email = request.POST['email']
        password = request.POST['password']
        
        # checks if it correspond to what is in the database and what the user submitted
        user = auth.authenticate(email=email, password=password)
        
        if user is not None:
            # here is the try-except block which checks the user cart_id and cartitem if they exists for a user.If it does, then assign it to the user account and update thier cartitem
            try:
                # this here i am trying to get the session id and assigns it to the cart_id. If yes...
                cart = Cart.objects.get(cart_id=_cart_id(request))
                # check if the cart exists or not
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists() #the cart in the database is equal to the cart up there
                
                if is_cart_item_exists:
                    # we get the cart item and then assigns it to the current user
                    cart_item = CartItem.objects.filter(cart=cart)
                    # we are going to loop over this cart item and then assign the looped item to the user
                    
                    # the current product variation the actually submits
                    product_variation = []
                    # we gotta loop over that cart_item up there, and append in to the product variation
                    for item in cart_item:
                        variations = item.variations.all()
                        # always remember to make it into a list
                        product_variation.append(list(variations))
                        
                    # filter this based on the user
                    cart_item = CartItem.objects.filter(user=user)
                    ex_var_list = []
                    id = []
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)
                        
                    # now, it is time to loop over the product_variation aka current_variation saved by the user
                    for pr in product_variation:
                        if pr in ex_var_list:
                            # get the index of pr in the existing variation list
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            # adds the current quantity if it matches, assign it to the current user and then save it
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            # this here is for a user that hasn't logged in
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                # remember, the cartitem has a field 'user' which is a foreign key to the Account model
                                item.user = user  #item.user is access the database  and the user is the current user about to login
                                item.save()
            except:
                pass
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    next_page = params['next']
                    return redirect(next_page)
            except:
                return redirect('accounts:dashboard')
        
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('accounts:login')
    
    
    return render(request, 'accounts/login.html')



@login_required(login_url='accounts:login')
def logout(request):
    auth.logout(request)
    messages.success(request,'You have logged out.')
    return redirect('accounts:login')


def activate(request, uidb64, token):
    # first we hae to use the try-except block
    try:
        # we are going to decode the user primary key
        
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations, your account has been activated.')
        return redirect('accounts:login')
    else:
        messages.error('Invalid activation link')
        return redirect('accounts:register')
    

@login_required(login_url='accounts:login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        # this here checks if the accounts of the user exists
        if Account.objects.filter(email=email).exists():
            # this here is very case-sensitive
            user = Account.objects.get(email__exact=email)
            # reset user password by sending them an email
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/reset_password_verification.html', {
                'user': user,
                'domain' : current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            
            to_mail = email
            send_email = EmailMessage(mail_subject, message, to=[to_mail])
            send_email.send()
            
            messages.success(request, 'Password reset link has been sent to'+[email])
            
            return redirect('accounts:login')
        
        else:
            messages.error(request, 'Your Account does not exist!')
            return redirect('accounts:forgot_password')
        
    return render(request, 'accounts/forgot_password.html')


def reset_password_validate(request, uidb64, token):
    try:
    # we are going to decode the user primary key

        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
    #save the user ID in a session which will be used later to reset the password of the user
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('accounts:reset_password')
    else:
        messages.error(request, 'This link has expired')
        return redirect('accounts:login')
    
    
# reset the password
def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            # i have to get the the user ID from the session
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset was successful.')
            return redirect('accounts:login')
        
        else:
            messages.error(request, 'Password did not match! Password should be 8 characters')
            return redirect('accounts:reset_password')
    else:
        return render(request, 'accounts/reset_password.html')