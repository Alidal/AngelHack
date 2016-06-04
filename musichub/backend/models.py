import os
import pygit2 as git

from django.db import models
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


class Commit(models.Model):
    description = models.TextField()
    hash = models.CharField(max_length=45, primary_key=True)
    time = models.DateTimeField(auto_now_add=True)
    track = models.ForeignKey('track.Track', related_name='commits')

    @classmethod
    def create(cls, description, file, track, initial=False):
        if initial:
            # Also we need to create Git repository with initial commit
            repository = git.init_repository(os.path.join(settings.GIT_ROOT,
                                                          track.owner.username,
                                                          track.title),
                                             False)
            track.repository = repository.path
            track.save()

        # Generate commit with given name. Also need to generate changes.
        repository = git.Repository(track.repository)

        # Save file to disk
        file_path = os.path.join(repository.workdir, track.title)
        default_storage.delete(file_path)
        default_storage.save(file_path, ContentFile(file.read()))
        # Add file to commit
        index = repository.index
        index.add_all()
        tree = index.write_tree()
        # Add authors
        author = git.Signature(track.owner.username, track.owner.email)
        committer = author
        # Get parents list
        commits = Commit.objects.filter(track=track).order_by('time').values_list('hash', flat=True)

        commit_hash = repository.create_commit("refs/heads/master",
                                               author, committer,
                                               description,
                                               tree,
                                               list(commits))
        obj = cls(description=description, track=track, hash=str(commit_hash))
        obj.save()
