from django.views.generic.base import View
from django.contrib.auth.models import User
from django.shortcuts import render

from track.models import Track
from backend.models import Commit


class AddTrackView(View):
    def post(self, request):
        data = request.POST
        user = User.objects.get(pk=self.request.user.pk)
        Track.create(title=data['title'],
                     file=data['file'],
                     owner=user)


class DifferenceView(View):
    template_name = 'repo/diff.html'

    def get(self, request):
        old_hash = request.GET['old']
        new_hash = request.GET['new']
        instrument = request.GET.get('instrument', None)
        old = Commit.objects.get(hash=old_hash)
        new = Commit.objects.get(hash=new_hash)
        diff = old.difference(new)
        if not instrument:
            instrument = diff['before'].keys()[0]
        context = {
            'user': old.track.owner,
            'track': old.track,
            'old_hash': old_hash,
            'new_hash': new_hash,
            'old': diff['before'][instrument]['source'],
            'new': diff['after'][instrument]['source'],
            'changes': diff['before'][instrument]['changes'],
            'instrument': instrument,
            'instruments': [k for k in diff['before'].keys() if k != instrument]
        }
        return render(request, self.template_name, context)
# class AddTrackView(FormView):

#     def form_valid(self, form):
#         data = form.cleaned_data
#         user = User.objects.get(pk=self.request.user.pk)
#         try:
#             obj = Track.objects.get(title=data['title'], owner=user)
#             # If track exists, we need to update it
#             obj.update(description=data['description'],
#                        new_file=data['file'])
#         except Track.DoesNotExist:
#             Track.create(title=data['title'],
#                          owner=user,
#                          file=data['file'])
#         return super().form_valid(form)
