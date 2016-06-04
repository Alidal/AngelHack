from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'signup'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Sign Up', css_class="btn-success"))

    class Meta(UserCreationForm.Meta):
        fields = ('email',) + UserCreationForm.Meta.fields


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'login'
        self.helper.form_method = 'post'

        self.helper.add_input(Submit('submit', 'Login', css_class="btn-success"))