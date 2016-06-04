from django.views.generic.edit import FormView
from django.contrib.auth.models import User

from track.forms import AddTrackForm
from track.models import Track


class AddTrackView(FormView):
    form_class = AddTrackForm
    template_name = "upload.html"
    success_url = '/'

    def form_valid(self, form):
        data = form.cleaned_data
        user = User.objects.get(pk=self.request.user.pk)
        try:
            obj = Track.objects.get(title=data['title'], owner=user)
            # If track exists, we need to update it
            obj.update(description=data['description'],
                       new_file=data['file'])
        except Track.DoesNotExist:
            Track.create(title=data['title'],
                         owner=user,
                         file=data['file'])
        return super().form_valid(form)
