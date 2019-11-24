from django.db import models


class Artist(models.Model):
    """
    Model for the single artist.
    """

    name = models.CharField(max_length=128)


class Track(models.Model):
    """
    Model for the single track.
    """

    id = models.CharField(max_length=32, primary_key=True, unique=True)
    name = models.CharField(max_length=128)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.artist.name}"


class Album(models.Model):
    """
    Model for the single album.
    """

    id = models.CharField(max_length=32, primary_key=True, unique=True)
    name = models.CharField(max_length=128)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    image = models.URLField(null=True)

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

    def get_features(self):
        return [
            self.danceability,
            self.speechiness,
            self.acousticness,
            self.valence,
            self.instrumentalness,
            self.energy,
            self.liveness,
        ]

    def get_features_for_chart(self):
        features = self.get_features()
        return [int(feat * 100) for feat in features]

    @staticmethod
    def calculate_album_features(spotify, tracks):
        dict_of_features = {
            "danceability": [],
            "speechiness": [],
            "acousticness": [],
            "valence": [],
            "instrumentalness": [],
            "energy": [],
            "liveness": [],
        }
        tracks_number = len(tracks)

        for track in tracks:
            track = spotify.get_track_audio_features(track["id"])
            for key in dict_of_features.keys():
                dict_of_features[key].append(track[key])

        for key in dict_of_features.keys():
            dict_of_features[key] = sum(dict_of_features[key]) / tracks_number

        return dict_of_features


class TrackFeatures(models.Model):

    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    features = models.ForeignKey(Features, on_delete=models.CASCADE)


class AlbumFeatures(models.Model):

    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    features = models.ForeignKey(Features, on_delete=models.CASCADE)
