from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout
from django.views.generic.edit import FormView
from django.views.generic.base import View
from basic.forms import RegistrationForm, LoginForm


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/")


class RegistrationView(FormView):
    form_class = RegistrationForm
    success_url = "/"
    template_name = "auth/register.html"

    def form_valid(self, form):
        form.save()
        user = form.instance
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(self.request, user)
        return super().form_valid(form)


class LoginView(FormView):
    form_class = LoginForm
    template_name = "auth/login.html"
    success_url = "/"

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super().form_valid(form)
