# Generated by Django 5.1.3 on 2024-12-12 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search_engine', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='song_cover',
            field=models.ImageField(blank=True, null=True, upload_to='api_data_img', verbose_name='spotify_song_cover'),
        ),
    ]
