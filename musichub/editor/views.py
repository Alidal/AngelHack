import json
from io import StringIO

from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View

from track.models import Track
from backend.models import Commit


class RepositoryView(View):
    template_name = 'repo/repo.html'

    def get(self, request, username, pk):
        track = Track.objects.get(pk=pk)
        if request.GET.get("commit") and Commit.objects.filter(track=track).count() > 1:
            commit = Commit.objects.get(hash=request.GET['commit'])
            notes = commit.get_source()
        else:
            notes = track.get_track()
            commit = track.commits.all().order_by('-time').last()

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
            'instruments': notes.keys(),
            'commit': commit
        }
        return render(request, self.template_name, context)


class EditorView(RepositoryView):
    template_name = 'repo/edit.html'


class SaveView(View):
    def post(self, request):
        data = request.POST
        track = Track.objects.get(pk=data['data']['repo_pk'])
        instrument = data['data']['instrument']

        source = track.get_track()
        source[instrument] = data['notes']
        file = StringIO(json.dumps(source))
        track.update(data['description'], file)

        return JsonResponse({"success": True})
