from registration.views import RegistrationView as DjangoRegistrationView
from basic.forms import RegistrationForm


class RegistrationView(DjangoRegistrationView):
    form_class = RegistrationForm
