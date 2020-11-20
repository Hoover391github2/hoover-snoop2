# Generated by Django 2.0.4 on 2018-10-19 14:21

from django.db import migrations, models
import django.db.models.deletion


def ensure_one_collection(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    Collection = apps.get_model('data', 'Collection')
    if len(Collection.objects.using(db_alias).all()) > 1:
        raise RuntimeError("Must have at most one collection")


def remove_collections(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    Task = apps.get_model('data', 'Task')
    for func in ['digests.gather', 'digests.launch', 'digests.index']:
        for task in Task.objects.using(db_alias).filter(func=func).iterator():
            task.args = task.args[:1] + task.args[2:]
            task.save()


def do_nothing(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0028_auto_20180525_2126'),
    ]

    operations = [
        migrations.RunPython(ensure_one_collection, do_nothing),
        migrations.RemoveField(
            model_name='directory',
            name='collection',
        ),
        migrations.RemoveField(
            model_name='file',
            name='collection',
        ),
        migrations.AlterField(
            model_name='digest',
            name='blob',
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.DO_NOTHING, to='data.Blob'),
        ),
        migrations.AlterUniqueTogether(
            name='digest',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='digest',
            name='collection',
        ),
        migrations.DeleteModel(
            name='Collection',
        ),
        migrations.RunPython(remove_collections, do_nothing),
    ]
