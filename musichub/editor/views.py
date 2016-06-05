from django.shortcuts import render
from django.views.generic import View

from track.models import Track
from backend.models import Commit


class RepositoryView(View):
    template_name = 'repo/repo.html'

    def get(self, request, username, pk):
        track = Track.objects.get(pk=pk)
        if request.GET.get("commit") and Commit.objects.filter(track=track).count() > 1:
            notes = Commit.objects.get(hash=request.GET['commit']).get_source()
        else:
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


class EditorView(RepositoryView):
    template_name = 'repo/edit.html'
