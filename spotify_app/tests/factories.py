import string

import factory
import factory.fuzzy

from spotify_app import models

CHAR_SET = string.ascii_letters + string.digits


class ArtistFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Artist

    id = factory.fuzzy.FuzzyText(length=24, chars=CHAR_SET)
    name = factory.Faker('name') 


class TrackFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Track

    id = factory.fuzzy.FuzzyText(length=24, chars=CHAR_SET)
    name = factory.Faker('sentence', nb_words=6, variable_nb_words=True, ext_word_list=None)

    artist = factory.SubFactory(ArtistFactory)


class AlbumFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Album

    id = factory.fuzzy.FuzzyText(length=24, chars=CHAR_SET)
    name = factory.Faker('sentence', nb_words=3, variable_nb_words=True, ext_word_list=None)
    image = factory.Faker('image_url')

    artist = factory.SubFactory(ArtistFactory)
    @factory.post_generation
    def tracks(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for track in extracted:
                self.tracks.add(track)


class FeaturesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Features

    danceability = factory.Faker(
        'pydecimal',
        left_digits=1,
        right_digits=3,
        positive=True,
        min_value=0,
        max_value=1
    )
    speechiness = factory.Faker(
        'pydecimal',
        left_digits=1,
        right_digits=3,
        positive=True,
        min_value=0,
        max_value=1
    )
    acousticness = factory.Faker(
        'pydecimal',
        left_digits=1,
        right_digits=3,
        positive=True,
        min_value=0,
        max_value=1
    )
    valence = factory.Faker(
        'pydecimal',
        left_digits=1,
        right_digits=3,
        positive=True,
        min_value=0,
        max_value=1
    )
    instrumentalness = factory.Faker(
        'pydecimal',
        left_digits=1,
        right_digits=3,
        positive=True,
        min_value=0,
        max_value=1
    )
    energy = factory.Faker(
        'pydecimal',
        left_digits=1,
        right_digits=3,
        positive=True,
        min_value=0,
        max_value=1
    )
    liveness = factory.Faker(
        'pydecimal',
        left_digits=1,
        right_digits=3,
        positive=True,
        min_value=0,
        max_value=1
    )


class TrackFeaturesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.TrackFeatures

    track = factory.SubFactory(TrackFactory)
    features = factory.SubFactory(FeaturesFactory)


class AlbumFeaturesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.AlbumFeatures

    track = factory.SubFactory(AlbumFactory)
    features = factory.SubFactory(FeaturesFactory)
