from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import connection
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
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
    return render(request, 'registration/login.html')

def logout_view(request):
    logout(request)
    # Redirect to the URL specified in LOGOUT_REDIRECT_URL
    return redirect('/login/')

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'registration/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('/login/')
