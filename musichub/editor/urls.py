from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from editor.views import RepositoryView, EditorView, SaveView


urlpatterns = [
    url(r'^track/save/?$', csrf_exempt(SaveView.as_view())),
    url(r'^(?P<username>[-\w.]+)/(?P<pk>[0-9]+)/?$', RepositoryView.as_view()),
    url(r'^(?P<username>[-\w.]+)/(?P<pk>[0-9]+)/edit/?$', EditorView.as_view()),
]
