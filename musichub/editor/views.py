from django.shortcuts import render
from django.views.generic import View

from track.models import Track
from track.converter import convert


class EditorView(View):
    template_name = 'repo/repo.html'

    def get(self, request):
        value = convert(Track.objects.last())['James Alan Hetfield']
        return render(request, self.template_name, {'result': value})
