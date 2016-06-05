from django.views.generic.base import View
from django.views.generic.list import ListView
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import JsonResponse, Http404

from track.models import Track
from backend.models import Commit


class AddTrackView(View):
    """
    AJAX view for new repo creation.
    """
    def post(self, request):
        data = request.POST
        user = User.objects.get(pk=self.request.user.pk)
        if 'id_commitdescription' in data:
            # For commit
            track = Track.objects.get(pk=data['pk'])
            track.update(description=data['id_commitdescription'],
                         new_file=request.FILES['file'])
        else:
            # For repository
            if Track.objects.filter(title=data['id_repotitle'],
                                    owner=user).exists():
                return JsonResponse({"success": False})

            Track.create(title=data['id_repotitle'],
                         file=request.FILES['file'],
                         owner=user)
        return JsonResponse({"success": True})


class DifferenceView(View):
    template_name = 'repo/diff.html'

    def get(self, request):
        old_hash = request.GET['old']
        new_hash = request.GET['new']
        instrument = request.GET.get('instrument', None)
        old = Commit.objects.get(hash=old_hash)
        new = Commit.objects.get(hash=new_hash)

        # Check if we take commits for th same repository
        if old.track != new.track:
            raise Http404

        diff = old.difference(new)
        if not instrument:
            instrument = list(diff['before'].keys())[0]
        context = {
            'user': old.track.owner,
            'track': old.track,
            'old_hash': old_hash,
            'new_hash': new_hash,
            'old': diff['before'][instrument]['source'],
            'new': diff['after'][instrument]['source'],
            'changes': diff['before'][instrument]['difference'],
            'instrument': instrument,
            'instruments': [k for k in diff['before'].keys() if k != instrument]
        }
        return render(request, self.template_name, context)


class CommitsListView(ListView):
    model = Commit
    template_name = "repo/commits.html"

    def get_queryset(self):
        return Commit.objects.filter(track__pk=self.kwargs['repo_pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['track'] = Track.objects.get(pk=self.kwargs['repo_pk'])
        return context
