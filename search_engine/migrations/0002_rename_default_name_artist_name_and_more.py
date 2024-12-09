# Generated by Django 5.1.3 on 2024-11-09 00:28

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search_engine', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='artist',
            old_name='default_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='song',
            old_name='anime_name',
            new_name='anime',
        ),
        migrations.RenameField(
            model_name='song',
            old_name='artist_name',
            new_name='artist',
        ),
        migrations.AddField(
            model_name='song',
            name='song_type',
            field=models.CharField(default=django.utils.timezone.now, max_length=10),
            preserve_default=False,
        ),
    ]
