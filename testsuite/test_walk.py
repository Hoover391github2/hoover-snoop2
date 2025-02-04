import pytest

from snoop.data import tasks
from snoop.data import filesystem
from snoop.data import models
from snoop.data import collections

from conftest import mask_out_current_collection

pytestmark = [pytest.mark.django_db]


def test_walk(taskmanager, monkeypatch):
    monkeypatch.setattr(
        collections.Collection,
        'DATA_DIR',
        'data/emlx-4-missing-part',
    )
    root = models.Directory.objects.create()

    filesystem.walk(root.pk)

    [file] = models.File.objects.all()
    hash = '442e8939e3e367c4263738bbb29e9360a17334279f1ecef67fa9d437c31804ca'
    assert file.original.pk == hash
    assert file.blob.pk == hash

    [task_pk] = taskmanager.queue
    task = models.Task.objects.get(pk=task_pk)
    assert task.func == 'filesystem.handle_file'
    assert task.args == [file.pk]


def test_smashed_filename(taskmanager, monkeypatch):
    monkeypatch.setattr(
        collections.Collection,
        'DATA_DIR',
        'data/disk-files/bad-filename',
    )
    root = models.Directory.objects.create()
    filesystem.walk(root.pk)

    assert len(models.File.objects.all()) == 2
    # hash = 'a8009a7a528d87778c356da3a55d964719e818666a04e4f960c9e2439e35f138'
    # assert file.original.pk == hash
    # assert file.name == broken_name


def test_children_of_archives_in_multiple_locations(taskmanager, monkeypatch):
    monkeypatch.setattr(
        collections.Collection,
        'DATA_DIR',
        'data/zip-in-multiple-locations',
    )
    models.Directory.objects.create()

    with mask_out_current_collection():
        tasks.run_dispatcher()

    taskmanager.run(limit=10000)

    files = list(models.File.objects.all())
    dirs = list(models.Directory.objects.all())

    [z1, c1, z2, c2] = sorted(files, key=lambda x: str(x.parent) + str(x))
    assert z1.blob == z2.blob
    assert c1.blob == c2.blob

    assert [(str(x), list(x.child_file_set.all())) for x in sorted(dirs, key=str)] == [
        ('/', []),
        ('/location-1/', [z1]),
        ('/location-1/parent.zip//', []),
        ('/location-1/parent.zip//parent/', [c1]),
        ('/location-2/', [z2]),
        ('/location-2/parent.zip//', []),
        ('/location-2/parent.zip//parent/', [c2])
    ]
    d1 = sorted(dirs, key=str)[2]
    d2 = sorted(dirs, key=str)[5]
    assert d1.child_directory_set.all()[0].parent == d1
    assert d1.parent == z1
    assert d2.child_directory_set.all()[0].parent == d2
    assert d2.parent == z2
