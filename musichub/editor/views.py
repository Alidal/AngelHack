from django.shortcuts import render
from django.views.generic import View

from track.models import Track


class EditorView(View):
    template_name = 'repo/repo.html'

    def get(self, request, username, pk):
        track = Track.objects.get(pk=pk).get_track()
        if request.GET.get('branch', None):
            value = track[request.GET['branch']]
        else:
            key, value = track.popitem()
        return render(request, self.template_name, {'track': value})
