from django.conf.urls import url

from basic.views import RegistrationView, LoginView, LogoutView, ProfileView


urlpatterns = [
    # Add custom registration view
    url(r'^signup/?$', RegistrationView.as_view()),
    url(r'^login/?$', LoginView.as_view()),
    url(r'^logout/?$', LogoutView.as_view()),
    url(r'^(?P<username>[-\w.]+)/?$', ProfileView.as_view()),
]
