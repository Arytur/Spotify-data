from django.db import models


class Track(models.Model):
    track_id = models.CharField(max_length=32, unique=True)
    track_artist = models.CharField(max_length=128)
    track_name = models.CharField(max_length=128)
    danceability = models.FloatField()
    speechiness = models.FloatField()
    acousticness = models.FloatField()
    valence = models.FloatField()
    instrumentalness = models.FloatField()
    energy = models.FloatField()
    liveness = models.FloatField()

    def __str__(self):
        return self.track_artist + ' - ' + self.track_name


class Album(models.Model):
    album_id = models.CharField(max_length=32, unique=True)
    album_artist = models.CharField(max_length=128)
    album_name = models.CharField(max_length=128)
    danceability = models.FloatField()
    speechiness = models.FloatField()
    acousticness = models.FloatField()
    valence = models.FloatField()
    instrumentalness = models.FloatField()
    energy = models.FloatField()
    liveness = models.FloatField()

    def __str__(self):
        return self.album_artist + ' - ' + self.album_name
