from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout
from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic.edit import FormView
from django.views.generic.base import View
from personal.forms import RegistrationForm, LoginForm
from track.models import Track


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
        if hasattr(self.user, 'username'):
            self.success_url = "/%s" % self.user.username
        return super().form_valid(form)


class ProfileView(View):
    template_name = "profile.html"

    def get(self, request, username):
        user = User.objects.get(username=username)
        tracks = Track.objects.filter(owner=user)
        context = {
            'user': user,
            'tracks': tracks
        }
        return render(request, self.template_name, context)
