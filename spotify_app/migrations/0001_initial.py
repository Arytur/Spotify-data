# Generated by Django 2.2.7 on 2019-12-09 21:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.CharField(max_length=32, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=128)),
                ('image', models.URLField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.CharField(max_length=32, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Features',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('danceability', models.DecimalField(decimal_places=3, max_digits=4)),
                ('speechiness', models.DecimalField(decimal_places=3, max_digits=4)),
                ('acousticness', models.DecimalField(decimal_places=3, max_digits=4)),
                ('valence', models.DecimalField(decimal_places=3, max_digits=4)),
                ('instrumentalness', models.DecimalField(decimal_places=3, max_digits=4)),
                ('energy', models.DecimalField(decimal_places=3, max_digits=4)),
                ('liveness', models.DecimalField(decimal_places=3, max_digits=4)),
            ],
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.CharField(max_length=32, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=128)),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spotify_app.Artist')),
            ],
        ),
        migrations.CreateModel(
            name='TrackFeatures',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('features', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spotify_app.Features')),
                ('track', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spotify_app.Track')),
            ],
        ),
        migrations.CreateModel(
            name='AlbumFeatures',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spotify_app.Album')),
                ('features', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spotify_app.Features')),
            ],
        ),
        migrations.AddField(
            model_name='album',
            name='artist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spotify_app.Artist'),
        ),
        migrations.AddField(
            model_name='album',
            name='tracks',
            field=models.ManyToManyField(to='spotify_app.Track'),
        ),
    ]
