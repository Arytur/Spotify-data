from django.db import models


class Track(models.Model):
    track_id = models.CharField(max_length=32, unique=True)
    track_artist = models.CharField(max_length=128)
    track_name = models.CharField(max_length=128)
    danceability = models.DecimalField(max_digits=4, decimal_places=3)
    speechiness = models.DecimalField(max_digits=4, decimal_places=3)
    acousticness = models.DecimalField(max_digits=4, decimal_places=3)
    valence = models.DecimalField(max_digits=4, decimal_places=3)
    instrumentalness = models.DecimalField(max_digits=4, decimal_places=3)
    energy = models.DecimalField(max_digits=4, decimal_places=3)
    liveness = models.DecimalField(max_digits=4, decimal_places=3)

    def __str__(self):
        return self.track_artist + ' - ' + self.track_name

    def get_features(self):
        return [
            self.danceability,
            self.speechiness,
            self.acousticness,
            self.valence,
            self.instrumentalness,
            self.energy,
            self.liveness
        ]

    def get_features_for_chart(self):
        features = self.get_features()
        return [int(feat * 100) for feat in features]


class Album(models.Model):
    album_id = models.CharField(max_length=32, unique=True)
    album_artist = models.CharField(max_length=128)
    album_name = models.CharField(max_length=128)
    danceability = models.DecimalField(max_digits=4, decimal_places=3)
    speechiness = models.DecimalField(max_digits=4, decimal_places=3)
    acousticness = models.DecimalField(max_digits=4, decimal_places=3)
    valence = models.DecimalField(max_digits=4, decimal_places=3)
    instrumentalness = models.DecimalField(max_digits=4, decimal_places=3)
    energy = models.DecimalField(max_digits=4, decimal_places=3)
    liveness = models.DecimalField(max_digits=4, decimal_places=3)
    
    def __str__(self):
        return self.album_artist + ' - ' + self.album_name
