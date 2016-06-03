from django.db import models
from django.contrib.auth.models import User

from backend.models import Commit


class Track(models.Model):
    """
    Also represents Git repository. One track - one repository.
    """

    title = models.CharField(max_length=256)
    owner = models.ForeignKey(User, related_name="track_owner")
    editors = models.ManyToManyField(User, related_name="track_editors")
    repository = models.CharField(max_length=256, default="")
    # commits is field for Commits model, that has reverse connection

    class Meta:
        unique_together = ('owner', 'title')

    def __init__(self, title, owner, file):
        self.title = title
        self.owner = owner
        self.editors.add(self.owner)
        # Create initial commit (automatically creates new repository)
        Commit.create("Initial commit", file, self, initial=True)

    def update(self, description, new_file, *args, **kwargs):
        Commit.create(description, new_file, self)
        super().save(self)
