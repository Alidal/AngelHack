from django.db import models
from django.contrib.auth.models import User

from backend.models import Commit


class Track(models.Model):
    """
    Also represents Git repository. One track - one repository.
    """
    title = models.CharField(max_length=256)
    owner = models.ForeignKey(User, related_name="track_owner")
    editors = models.ManyToManyField(User, related_name="track_editors", blank=True)
    repository = models.CharField(max_length=256, default="")
    # commits is field for Commits model, that has reverse connection

    class Meta:
        unique_together = ('owner', 'title')

    def __str__(self):
        return "%s - %s" % (self.owner.username, self.title)

    @classmethod
    def create(cls, title, owner, file):
        obj = cls(title=title, owner=owner)
        obj.title = title
        obj.owner = owner
        # Create initial commit (automatically creates new repository)
        Commit.create("Initial commit", file, obj, initial=True)
        obj.save()

    def update(self, description, new_file, *args, **kwargs):
        Commit.create(description, new_file, self)
