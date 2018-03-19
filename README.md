# Spotify-data
Django project based on Spotify API. 

This is my final project created at Coderslab Bootcamp - Python Backend Developer.

![Image](https://github.com/Arytur/Spotify-data/blob/master/spot1.png?raw=true)

With this application it is possible to requests data from Spotify such as:
* list of new released albums
* overview an album - all songs and image of the album
* list of recently listened songs by user
* search an artist's albums

But the most important to me was the data delivered together with almost every song. They are so called "audio feature information" and they describe values such as: *danceability, speechiness, acousticness, valence, instrumentalness, energy, liveness*. All of them are in the range 0 to 1. So it was a great opportunity to use them to collect the information about particular song or to calculate the average of whole album and display the result in the form of a graph. Once the data is displayed it is stored in the database, so in the next template it is possible to collect them all together in one table. Now we have possibility to compare all stored data and order them by values which we are interested in. 

![Image](https://github.com/Arytur/Spotify-data/blob/master/spot2.png?raw=true)


This project was created with use:
* Django ver.1.11.6 + requests library
* jquery
* bootstrap

## How to install:
1. You need to create/register your own application on Spotify website [tutorial here](https://developer.spotify.com/web-api/tutorial/) 
2. On Spotify website find 'My Apps' section and set the address of your website to http://127.0.0.1:8000/ and the address of Redirect URIs to  http://127.0.0.1:8000/callback/q
3. In return you receive 'Client ID' and 'Client Secret' - you need them to authenticate yourself. Paste these values in the right places in keys.json file in the main folder of the project.


-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

The repository which helped me a lot:

https://github.com/plamere/spotipy

I couldn't use it directly with my project, because it was created in python 2 and flask, so some changes was needed.
