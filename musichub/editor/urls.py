from django.conf.urls import url
from editor.views import EditorView


urlpatterns = [
    url(r'^repo$', EditorView.as_view()),
]
