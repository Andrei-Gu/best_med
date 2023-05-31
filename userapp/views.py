from django.views.generic import CreateView
from .models import MedServiceUser
from .forms import *
from django.contrib.auth.views import LoginView, LogoutView

class UserRegistrationView(CreateView):
    model = MedServiceUser
    template_name = 'userapp/user_registration_form.html'
    form_class = UserRegistrationForm
    success_url = '/login/'

class UserLoginView(LoginView):
    template_name = 'userapp/user_login_form.html'
    form_class = UserLoginForm


class UserLogoutView(LogoutView):
    pass

