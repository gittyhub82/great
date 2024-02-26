from django.db import models
from django.contrib.auth.models import  AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('User must have an email Address')
        
        if not username:
            raise ValueError('User must have an username')
        
        user = self.model(
            #Normalize the email address by lowercasing the domain part of it.
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name
        )
        
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    
    def create_superuser(self, first_name, last_name, username, email, password):
        user = self.create_user(
            email = self.normalize_email(email),
            first_name= first_name,
            last_name = last_name,
            username= username,
            password=password,
        )
        
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user
            




# This class creates users for your app
class Account(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=50)   
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50)
    
    objects = MyAccountManager()
    # required fields to actually override the AbstractBaseUser
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name'
    ]
    
    def __str__(self) -> str:
        return self.email
    
    
    def has_perm(self, perm, obj=None):
       return self.is_admin
   
    def has_module_perms(self, add_label):
       return True