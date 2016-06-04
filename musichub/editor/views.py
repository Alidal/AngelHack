from django.shortcuts import render
from django.views.generic import View

from track.models import Track


class EditorView(View):
    template_name = 'repo/repo.html'

    def get(self, request, username, pk):
        track = Track.objects.get(pk=pk)
        notes = track.get_track()
        if request.GET.get('instrument', None):
            key = request.GET['instrument']
            value = notes[key]
            del notes[key]
        else:
            key, value = notes.popitem()
        context = {
            'notes': value,
            'track': track,
            'instrument': key,
            'instruments': notes.keys()
        }
        return render(request, self.template_name, context)
