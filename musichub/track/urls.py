from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from track.views import AddTrackView


urlpatterns = [
    url(r'^upload$', login_required(AddTrackView.as_view())),
]
