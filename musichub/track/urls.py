from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from track.views import AddTrackView, DifferenceView


urlpatterns = [
    url(r'^(?P<username>[-\w.]+)/repository/create/?$', TemplateView.as_view(template_name='repo/new_repo.html')),
    url(r'^(?P<username>[-\w.]+)/(?P<repo_pk>[0-9]+)/commit/create/?$', TemplateView.as_view(template_name='repo/new_repo.html')),
    url(r'^(?P<username>[-\w.]+)/(?P<repo_pk>[0-9]+)/commit/list/?$', TemplateView.as_view(template_name='main.html')),
    url(r'^upload/?$', login_required(csrf_exempt(AddTrackView.as_view()))),
    url(r'^difference/?$', login_required(DifferenceView.as_view())),
]
