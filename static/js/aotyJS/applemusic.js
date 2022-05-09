//js goes here
//https://musickit.js.org/#/

require('dotenv').config({ path: '../../../.env' })

const MusicKit = require('node-musickit-api/personalized')
const fs = require('fs')


var music = new MusicKit({
  key: process.env.MUSICKIT_KEY, // Readss your private key
  teamId: process.env.APPLEDEV_TEAM_ID, // This is your developer account's team ID
  keyId: process.env.APPLEDEV_KEY_ID, // This is the keys ID
  userToken: "eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiIsImtpZCI6Ik1MSjJDVzY5WDgifQ.eyJpc3MiOiJSUU05TVRSOThSIiwiZXhwIjoxNjQ3NDcxNjE1LCJpYXQiOjE2NDY4NzA0MTV9.2E5gKgapE8rxjo3JFQhBTdqWInQdAUVyfp4ZwiltZD507eYpxUHAl2J7kHZvwIvvYXfehauitNhnbYy3k51yLw"
})



