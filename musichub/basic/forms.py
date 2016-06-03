from registration.forms import RegistrationForm as DjangoRegistrationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class RegistrationForm(DjangoRegistrationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'signup'
        self.helper.form_method = 'post'

        self.helper.add_input(Submit('submit', 'Sign Up', css_class="btn-success"))
