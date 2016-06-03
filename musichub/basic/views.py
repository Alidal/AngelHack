from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout
from django.views.generic.edit import FormView
from django.views.generic.base import View
from registration.views import RegistrationView as DjangoRegistrationView
from basic.forms import RegistrationForm, LoginForm


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/")


class RegistrationView(DjangoRegistrationView):
    form_class = RegistrationForm


class LoginView(FormView):
    form_class = LoginForm
    template_name = "registration/login.html"
    success_url = "/"

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super().form_valid(form)
