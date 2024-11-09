from django.db import models

class Anime(models.Model):
    default_title = models.CharField(max_length=100)
    eng_title = models.CharField(max_length=100)
    jp_title = models.CharField(max_length=100)

    def __str__(self):
        return self.default_title
        

class Artist(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Song(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    song_type = models.CharField(max_length=10)    
    song_name_roman = models.CharField(max_length=100)
    song_name_jp = models.CharField(max_length=100)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    #suggestion = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.song_name_roman
    
