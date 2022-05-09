//injects the album view modal with the relevant information
//gets the info from the DB

class Album{
    constructor(album_name, artist_name, artwork_url, genres, user){
        this.album_name = album_name;
        this.artist_name = artist_name;
        this.artwork_url = artwork_url;
        this.genres = genres;
        this.user = user; 
    }
}

function inject(){

    console.log(document.getElementById("aotyModal"));
}

let album_name = "Pleasant Dreams"
let artist_name = "The Ramones"
let artwork_url = "https://aotyhelper.com/album.png"
let genres = ['Punk', 'Ramonescore']
let user = "admin"

const release = new Album(album_name, artist_name, artwork_url, genres, user);

console.log(release)

//TODO: Theres a redeclaration issue in here somewhere
//TODO: Grab info from database