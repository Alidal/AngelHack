from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class AddTrackForm(forms.Form):
    file = forms.FileField()
    title = forms.CharField(max_length=50)
    description = forms.CharField(max_length=50)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'signup'
        self.helper.form_method = 'post'

        self.helper.add_input(Submit('submit', 'Upload', css_class="btn-success"))
