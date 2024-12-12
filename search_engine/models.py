from django.db import models

class Anime(models.Model):
    BROADCAST_TYPES = [
        ('TV', 'TV Series'),
        ('MV', 'Movie'),
        ('ONA', 'ONA'),
        ('OVA', 'OVA'),
        ('SP', 'Special'),
    ]

    anime_id_mal = models.CharField(primary_key=True, max_length=50, unique=True, verbose_name="Anime's MyAnimeList ID", default='ZXCV')
    roman_title = models.CharField(max_length=100, verbose_name="Romanized Title",null=True, blank=True)
    jp_title = models.CharField(max_length=100, null=True, blank=True, verbose_name="Japanese Title")
    broadcast_type = models.CharField(max_length=10, choices=BROADCAST_TYPES, verbose_name="Broadcasting Type",null=True)

    def __str__(self):
        return self.roman_title


class Artist(models.Model):
    artist_id_spotify = models.CharField(primary_key=True, max_length=50, unique=True, verbose_name="Artist's Spotify ID", default='ASDF')
    name = models.CharField(max_length=100, verbose_name="Artist Name",null=True, blank=True)

    def __str__(self):
        return self.name


class Song(models.Model):
    SONG_TYPES = [
        ('O', 'Opening'),
        ('E', 'Ending'),
        ('I', 'Insert'),
    ]
    REL_NAME_STR = 'songs'

    song_id_spotify = models.CharField(primary_key=True, max_length=50, unique=True, verbose_name="Song's Spotify ID", default='QWER')
    song_name_roman = models.CharField(max_length=100, db_index=True, verbose_name="Romanized Song Name",null=True, blank=True)
    song_name_jp = models.CharField(max_length=100, null=True, blank=True, db_index=True, verbose_name="Japanese Song Name")
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name=REL_NAME_STR, verbose_name="Artist", null=True)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name=REL_NAME_STR, verbose_name="Related Anime", null=True)
    song_type = models.CharField(max_length=10, choices=SONG_TYPES, db_index=True, verbose_name="Song Type",null=True)
    song_cover = models.ImageField(upload_to='api_data_img', verbose_name='spotify_song_cover', null=True, blank=True)

    def __str__(self):
        return self.song_name_roman
