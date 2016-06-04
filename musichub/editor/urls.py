from django.conf.urls import url
from editor.views import EditorView


urlpatterns = [
    url(r'^(?P<username>[-\w.]+)/(?P<pk>[0-9]+)/?$', EditorView.as_view()),
]
