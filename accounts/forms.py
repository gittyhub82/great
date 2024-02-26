from collections.abc import Mapping
from typing import Any
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList

from .models import *


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : 'Enter your password',
        #this is how you add a class field to your form field in django
        # class : form-control
    }))
    
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : 'Re-confirm your password',
    }))
    class Meta:
        model = Account
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'password',
        ]
        
            
    def clean(self):
        """currently trying to override the 'clean' method"""
        cleaned_data = super(RegistrationForm, self).clean()
        
        # now let's get the password and the confirm password so that a user as to put the right password before they can be validated
        
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        # if len(password) and len(confirm_password) < 8:
        #     raise forms.ValidationError('Password length must be more than eigth.')
        
        if password != confirm_password:
            raise forms.ValidationError('Password does not match!')
    # time to overwrite the current init method of the registration form
    
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, *kwargs)
        # here, we are going to assign the placeholders to the form fields that we have
        
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter Your First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Your Last Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Your Email Here'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Provide Your Phone Number'
        
        # looping through all the instances fields, and assiging them the class = form-control
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            
            