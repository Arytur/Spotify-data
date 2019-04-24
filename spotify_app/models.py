from django.db import models

from .tasks import SpotifyRequest


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
    album_image = models.URLField(null=True)
    danceability = models.DecimalField(max_digits=4, decimal_places=3)
    speechiness = models.DecimalField(max_digits=4, decimal_places=3)
    acousticness = models.DecimalField(max_digits=4, decimal_places=3)
    valence = models.DecimalField(max_digits=4, decimal_places=3)
    instrumentalness = models.DecimalField(max_digits=4, decimal_places=3)
    energy = models.DecimalField(max_digits=4, decimal_places=3)
    liveness = models.DecimalField(max_digits=4, decimal_places=3)
    
    def __str__(self):
        return self.album_artist + ' - ' + self.album_name

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

    @staticmethod
    def calculate_album_features(spotify, tracks):
        
        tracks_number = len(tracks)
        dict_of_features = {'danceability': [], 'speechiness': [], 'acousticness': [],
                        'valence': [], 'instrumentalness': [], 'energy': [], 'liveness': []}
        for track in tracks:
            track = spotify.get_track_audio_features(track['id'])
            dict_of_features['danceability'].append(track['danceability'])
            dict_of_features['speechiness'].append(track['speechiness'])
            dict_of_features['acousticness'].append(track['acousticness'])
            dict_of_features['valence'].append(track['valence'])
            dict_of_features['instrumentalness'].append(track['instrumentalness'])
            dict_of_features['energy'].append(track['energy'])
            dict_of_features['liveness'].append(track['liveness'])

        dict_of_features['danceability'] = sum(dict_of_features['danceability']) / tracks_number
        dict_of_features['speechiness'] = sum(dict_of_features['speechiness']) / tracks_number
        dict_of_features['acousticness'] = sum(dict_of_features['acousticness']) / tracks_number
        dict_of_features['valence'] = sum(dict_of_features['valence']) / tracks_number
        dict_of_features['instrumentalness'] = sum(dict_of_features['instrumentalness']) / tracks_number
        dict_of_features['energy'] = sum(dict_of_features['energy']) / tracks_number
        dict_of_features['liveness'] = sum(dict_of_features['liveness']) / tracks_number

        return dict_of_features
