require('dotenv').config({ path: `../../../.env`});
var request = require('request');
var cors = require('cors');
var querystring = require('querystring');
var axios = require('axios')

// Spotify End Points
const AUTH_ENDPOINT = 'https://accounts.spotify.com/authorize?'

// Query Params
var clientID = process.env.SPOTIFY_CLIENT_ID
var redirectURI = process.env.SPOTIFY_REDIRECT_URI
var scope = 'user-read-recently-played'
var responseType = 'code'




