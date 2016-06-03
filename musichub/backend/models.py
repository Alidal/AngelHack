import pygit2 as git

from django.db import models
from django.conf import settings


class Commit(models.Model):
    description = models.TextField()
    hash = models.CharField(max_length=45)
    time = models.DateTimeField(auto_now_add=True)
    track = models.ForeignKey('track.Track', related_name='commits')
    # changes = reverse connection

    def __init__(self, description, file, track, initial=False):
        super().__init__(self)
        import ipdb; ipdb.set_trace()
        self.description = description
        self.track = track

        if initial:
            # Also we need to create Git repository with initial commit
            repository_name = "%s-%s" % (track.owner.username, track.title)
            repository = git.init_repository(settings.GIT_ROOT + "/" + repository_name, False)
            track.repository = repository.path
            track.save()

        # Generate commit with given name. Also need to generate changes.
        repository = git.Repository(track.repository)
        repository.create_blob(file)
        author = git.Signature(track.owner.username, track.owner.email)
        committer = author
        tree = repository.TreeBuilder().write()
        commit_hash = repository.create_commit("refs/heads/master",
                                               author, committer,
                                               description,
                                               tree,
                                               [])
        self.hash = str(commit_hash)


# class Change(models.Model):
#     commit = models.ForeignKey(Commit, related_name='changes')
