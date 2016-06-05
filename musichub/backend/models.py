import os
import json
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

    def __str__(self):
        return "%s - %s" % (self.description, self.track.title)

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
        commits = Commit.objects.filter(track=track).order_by('-time').values_list('hash', flat=True)

        commit_hash = repository.create_commit("refs/heads/master",
                                               author, committer,
                                               description,
                                               tree,
                                               list(commits))
        obj = cls(description=description, track=track, hash=str(commit_hash))
        obj.save()

    def get_source(self):
        """
        A little bit tricky method for getting file state from commit.
        """
        repository = git.Repository(self.track.repository)
        commit = repository.revparse_single(self.hash)
        diff = commit.tree.diff_to_workdir().patch
        return json.loads(diff.patch.split('\n')[7][1:])

    def get_parent_commit_hash(self):
        repository = git.Repository(self.track.repository)
        commit = repository.revparse_single(self.hash)
        import ipdb; ipdb.set_trace()
        return commit.parents[-1].id if commit.parents else None

    def difference(self, commit):
        repository = git.Repository(self.track.repository)
        diff = repository.diff(self.hash, commit.hash)
        # I'm sorry
        before = json.loads(diff.patch.split('\n')[5][1:])
        after = json.loads(diff.patch.split('\n')[7][1:])

        result = {
            "before": {},
            "after": {}
        }
        for key, value in before.items():
            result['before'][key] = {}
            result['before'][key]['source'] = before[key]
            diffs = set(before[key].split('|')) - set(after[key].split('|'))
            diffs_indexes = [before[key].split('|').index(item) for item in diffs]
            result['before'][key]['difference'] = diffs_indexes

        for key, value in after.items():
            result['after'][key] = {}
            result['after'][key]['source'] = after[key]
            diffs = set(after[key].split('|')) - set(before[key].split('|'))
            diffs_indexes = [after[key].split('|').index(item) for item in diffs]
            result['after'][key]['difference'] = diffs_indexes
        return result
