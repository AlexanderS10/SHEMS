from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
    
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('An email is required')
        if not password:
            raise ValueError('A password is required for creating a user')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class Customer(AbstractUser):
    username = None #Let django manage the keys and how it does is by using its own id and that will be the customer_id
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    password = models.CharField(max_length=200, null=False, blank=False)
    first_name = models.CharField(max_length=30, null=False, blank=False)
    last_name = models.CharField(max_length=30, null=False, blank=False)
    billing_unit_number = models.SmallIntegerField(null=False, blank=False)
    billing_street_number = models.SmallIntegerField(null=False, blank=False)
    billing_street_name = models.CharField(max_length=30, null=False, blank=False)
    billing_city = models.CharField(max_length = 30, null=False, blank=False)
    billing_state = models.CharField(max_length=2, null=False, blank=False)
    billing_zipcode = models.CharField(max_length=5, null=False, blank=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["first_name", "last_name", "billing_unit_number", "billing_street_number", "billing_street_name", "billing_state","billing_zipcode"]
    objects = CustomUserManager()



