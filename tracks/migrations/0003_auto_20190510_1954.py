# Generated by Django 2.1.5 on 2019-05-10 11:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracks', '0002_auto_20190510_1951'),
    ]

    operations = [
        migrations.RenameField(
            model_name='features',
            old_name='artist',
            new_name='artist_id',
        ),
    ]
