from django.views.generic.edit import FormView
from track.forms import AddTrackForm
from track.models import Track


class AddTrackView(FormView):
    form_class = AddTrackForm
    template_name = "upload.html"
    success_url = '/'

    def form_valid(self, form):
        data = form.cleaned_data
        try:
            obj = Track.objects.get(title=data['title'], owner=self.request.user)
            # If track exists, we need to update it
            obj.update(description=data['description'],
                       new_file=data['file'])
        except Track.DoesNotExist:
            Track.create(title=data['title'],
                         owner=self.request.user,
                         file=data['file'])
        return super().form_valid(form)
