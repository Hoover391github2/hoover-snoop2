# Generated by Django 2.0.4 on 2018-05-09 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0026_auto_20180509_0936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='root',
            field=models.CharField(blank=True, max_length=4096),
        ),
    ]
