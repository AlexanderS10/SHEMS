from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.db import connection
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import RegistrationForm 
from accounts.models import Customer
from django.contrib import messages
# Create your views here.
def landing_view(request):
    return render(request, "landing/landing.html")

def signup_view(request):
    return render(request, "signup.html")

def custom_login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request,email=email, password = password)
        if user is not None:
            user_info = None
            with connection.cursor() as cursor:
                cursor.execute("SELECT first_name, last_name  FROM accounts_customer WHERE email=%s",[email])
                user_info = cursor.fetchone()
            request.session['user_info'] = user_info
            login(request, user)
            return redirect('/home/')
    return render(request, 'landing/login.html')

def logout_view(request):
    logout(request)
    # Redirect to the URL specified in LOGOUT_REDIRECT_URL
    return redirect('/login/')

class RegisterView(View):
    def get(self, request):
        form = RegistrationForm()  # Initialize the registration form
        return render(request, 'registration/register.html', {'form': form})
    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            required_fields = ['email', 'password1', 'password2', 'first_name', 'last_name', 'billing_unit_number', 'billing_street_number', 'billing_street_name', 'billing_city', 'billing_state', 'billing_zipcode']
            for field_name in required_fields:
                if not form.cleaned_data.get(field_name):
                    messages.error(request, f"{field_name.capitalize().replace('_', ' ')} is required.")
                    return render(request, 'registration/register.html', {'form': form})
            if form.cleaned_data['password1'] != form.cleaned_data['password2']:
                messages.error(request, "Passwords do not match.")
                return render(request, 'registration/register.html', {'form': form})
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            billing_unit_number = form.cleaned_data['billing_unit_number']
            billing_street_number = form.cleaned_data['billing_street_number']
            billing_street_name = form.cleaned_data['billing_street_name']
            billing_city = form.cleaned_data['billing_city']
            billing_state = form.cleaned_data['billing_state']
            billing_zipcode = form.cleaned_data['billing_zipcode']
            user = Customer.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name, billing_unit_number=billing_unit_number, billing_street_number=billing_street_number, billing_street_name=billing_street_name, billing_city=billing_city, billing_state=billing_state, billing_zipcode=billing_zipcode)
            messages.success(request, "You have successfully registered! Please log in.")  
            return redirect('login')  # Redirect to login page after successful registration
        
        return render(request, 'registration/register.html', {'form': form})

