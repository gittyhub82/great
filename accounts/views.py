from django.shortcuts import render, redirect
from .forms import *

from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from .models import *
# Create your views here.


# these are the imports you need to make for you to use the the token  to activate a user accounts
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage



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
            auth.login(request, user)
            # messages.success(request, 'You have logged in.')
            return redirect('category:index')
        
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