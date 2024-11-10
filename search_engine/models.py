from django.db import models

class Anime(models.Model):
    default_title = models.CharField(max_length=100)
    eng_title = models.CharField(max_length=100, null=True, blank=True)
    jp_title = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.default_title
        

class Artist(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Song(models.Model):
    SONG_TYPES = [
        ('O', 'Opening'),
        ('E', 'Ending'),
        ('I', 'Insert'),
    ]
    REL_NAME_STR = 'songs'
    
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name=REL_NAME_STR)
    song_type = models.CharField(max_length=10, choices=SONG_TYPES, db_index=True)    
    song_name_roman = models.CharField(max_length=100, db_index=True)
    song_name_jp = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name=REL_NAME_STR)
    #suggestion = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.song_name_roman
    
