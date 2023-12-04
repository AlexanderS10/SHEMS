from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.db import connection
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from django.shortcuts import redirect

def customer_home_view(request):
    user_info = request.session.get('user_info')
    return render(request, "customer/customer_home.html", {'user_info':user_info})


            