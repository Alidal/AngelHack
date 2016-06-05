import json
from io import StringIO

from django.db import models
from django.contrib.auth.models import User

from backend.models import Commit
from track.converter import convert


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
    def get_abc_from_file(self, file):
        # Can take GP5 or ABC files. Returns ABC
        try:
            # Convert from GP5 to ABC
            result = convert(file)
            return StringIO(json.dumps(result))
        except:
            # If file already in ABC format
            return StringIO(json.dumps({"Basic": file.read().decode('ascii')}))

    @classmethod
    def create(cls, title, owner, file):
        obj = cls(title=title, owner=owner)
        obj.title = title
        obj.owner = owner
        file = cls.get_abc_from_file(file)
        # Create initial commit (automatically creates new repository)
        Commit.create("Initial commit", file, obj, initial=True)
        obj.save()

    def update(self, description, new_file):
        new_file = self.get_abc_from_file(new_file)
        Commit.create(description, new_file, self)

    def get_track(self):
        file = open(self.repository.split('.')[0] + self.title, 'r+')
        return json.loads(file.read())
