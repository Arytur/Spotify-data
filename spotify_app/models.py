from django.db import models


class Artist(models.Model):
    """
    Model for single artist.
    """

    id = models.CharField(max_length=32, primary_key=True, unique=True)
    name = models.CharField(max_length=128)


class Track(models.Model):
    """
    Model for single track.
    """

    id = models.CharField(max_length=32, primary_key=True, unique=True)
    name = models.CharField(max_length=128)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.artist.name}"


class Album(models.Model):
    """
    Model for single album.
    """

    id = models.CharField(max_length=32, primary_key=True, unique=True)
    name = models.CharField(max_length=128)
    image = models.URLField(null=True)

    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    tracks = models.ManyToManyField(Track)

    def __str__(self):
        return f"{self.name} - {self.artist.name}"


class Features(models.Model):
    """
    additional features for track/albums
    """

    danceability = models.DecimalField(max_digits=4, decimal_places=3)
    speechiness = models.DecimalField(max_digits=4, decimal_places=3)
    acousticness = models.DecimalField(max_digits=4, decimal_places=3)
    valence = models.DecimalField(max_digits=4, decimal_places=3)
    instrumentalness = models.DecimalField(max_digits=4, decimal_places=3)
    energy = models.DecimalField(max_digits=4, decimal_places=3)
    liveness = models.DecimalField(max_digits=4, decimal_places=3)

    @property
    def get_fields_names(self):
        return [f.name for f in Features._meta.fields if f.name != 'id']

    @property
    def get_features(self):
        dict_of_features = {
            f: getattr(self, f) for f in self.get_fields_names
        }
        return dict_of_features

    def get_features_for_chart(self):
        return [int(feat * 100) for feat in self.get_features.values()]


class TrackFeatures(models.Model):

    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    features = models.ForeignKey(Features, on_delete=models.CASCADE)


class AlbumFeatures(models.Model):

    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    features = models.ForeignKey(Features, on_delete=models.CASCADE)
