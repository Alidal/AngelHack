from django.conf.urls import url
from editor.views import RepositoryView, EditorView


urlpatterns = [
    url(r'^(?P<username>[-\w.]+)/(?P<pk>[0-9]+)/?$', RepositoryView.as_view()),
    url(r'^(?P<username>[-\w.]+)/(?P<pk>[0-9]+)/edit/?$', EditorView.as_view()),
]
