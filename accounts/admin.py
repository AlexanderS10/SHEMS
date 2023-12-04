from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Customer  # Import your custom User model

@admin.register(Customer)
class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'is_staff']
    ordering = ['email']  # Replace 'username' with an existing field in your User model
    # Add other configurations as needed
