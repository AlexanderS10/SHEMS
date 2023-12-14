from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.db import connection, transaction
from django.shortcuts import redirect
from .forms import RegistrationForm 
from django.contrib import messages
# Create your views here.
def landing_view(request):
    return render(request, "landing/landing.html")

def signup_view(request):
    return render(request, "signup.html")

def custom_login(request):#Find where I can send an error message when the email or password is incorrect
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request,email=email, password = password)
        if user is not None:
            user_info = None
            with connection.cursor() as cursor:
                cursor.execute("SELECT first_name, last_name  FROM accounts_customers WHERE email=%s",[email])
                user_info = cursor.fetchone()
            request.session['user_info'] = user_info
            login(request, user)
            return redirect('/home/')
        else:
            messages.error(request, "Email or password is incorrect.")
            return render(request, 'landing/login.html')
    return render(request, 'landing/login.html')

def logout_view(request):
    logout(request)
    # Redirect to the URL specified in LOGOUT_REDIRECT_URL
    return redirect('/login/')

class RegisterView(View):
    def get(self, request):
        form = RegistrationForm()  # Initialize the registration form
        return render(request, 'landing/signup.html', {'form': form})
    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            required_fields = ['email', 'password1', 'password2', 'first_name', 'last_name', 'billing_unit_number', 'billing_street_number', 'billing_street_name', 'billing_city', 'billing_state', 'billing_zipcode']
            for field_name in required_fields:
                if not form.cleaned_data.get(field_name):
                    messages.error(request, f"{field_name.capitalize().replace('_', ' ')} is required.")
                    return render(request, 'landing/signup.html', {'form': form})
            if form.cleaned_data['password1'] != form.cleaned_data['password2']:
                messages.error(request, "Passwords do not match.")
                return render(request, 'landing/signup.html', {'form': form})
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
            with transaction.atomic():
                try:
                    with connection.cursor() as cursor:
                        cursor.execute(
                            '''
                            INSERT INTO accounts_customers (email, password, first_name, last_name, billing_unit_number, billing_street_number, billing_street_name, billing_city, billing_state, billing_zipcode, is_active)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, TRUE);
                            ''',
                            [email, password, first_name, last_name, billing_unit_number, billing_street_number, billing_street_name, billing_city, billing_state, billing_zipcode]
                        )
                    messages.success(request, "You have successfully registered! Please log in.")
                    return redirect('login')  # Redirect to login page after successful registration
                except Exception as e:
                    messages.error(request, f"An error occurred during registration: {e}")
                    return render(request, 'landing/signup.html', {'form': form})
        return render(request, 'landing/signup.html', {'form': form})


