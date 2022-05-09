# Django imports
from django.core.exceptions import ObjectDoesNotExist

# models
from .models import RecordLabel, Genre, Album, BandcampUserName, Artist, PlaysOn, Released, AlbumArt, ImageUrl, Describe, UserListenedTo

# Stdlib
import logging
logger = logging.getLogger('api_app')  # from LOGGING.loggers in settings.py


# Utilities class that houses a bunch of useful functions
class Utils():
    def __init__(self):

        # Logging Init
        logging.basicConfig(
                            filename="utils.log",
                            format='%(asctime)s %(message)s',
                            filemode='a'
                    )
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

    def labelExists(self, recordLabelstr):
        try:
            obj = RecordLabel.objects.get(recordLabelName=recordLabelstr)
            return True
        except ObjectDoesNotExist:
            recordLabel_obj = RecordLabel.objects.create()
            recordLabel_obj.recordLabelName = recordLabelstr
            recordLabel_obj.save()
            return True

    # 'Purely' Boolean Functions
    def album_exists(self, album_name):
        if Album.objects.filter(albumName=album_name).exists():
            return True
        return False

    def artist_exists(self, artist_name):
        if Artist.objects.filter(artistName=artist_name).exists():
            return True
        return False

    def playsOn_exists(self, album_name, artist_name):
        if PlaysOn.objects.filter(display_album_name=album_name, display_artist_name=artist_name).exists():
            return True
        return False

    def ultExists(self, user, album_name, artist_name):
        album_obj = Album.objects.get(albumName=album_name)
        artist_obj = Artist.objects.get(artistName=artist_name)
        if UserListenedTo.objects.filter(user=user, FK_albumID_userLT=album_obj.albumID, FK_artistID=artist_obj.artistID).exists():
            return True
        return False

    # Create a UserListenedTo Object
    def createUlt(self, user, album_name, artist_name):
        album_obj = Album.objects.get(albumName=album_name)
        artist_obj = Artist.objects.get(artistName=artist_name)
        ult_obj = UserListenedTo.objects.create(user=user, FK_albumID_userLT=album_obj, FK_artistID=artist_obj, FK_release_date_LT=album_obj.release_date)
        return ult_obj

    def user_already_listened(self, user, album_name, artist_name):
        if UserListenedTo.objects.filter(user=user, FK_albumID_userLT=Album.objects.get(albumName=album_name)).exists():
            return True
        else:
            return False

    # Retrieve the Bandcamp username
    def getBC_Username(self, request):
        # TODO: THIS
        return "bplistens"

    # Create an album object with every piece of scrapable data
    def createAlbum_FullOBJ(self, request, album_name, artist_name, release_date, record_label, img_url, *genre_tags):

        # check if album, artist exist
        if Album.objects.filter(albumName=album_name).exists() and Artist.objects.filter(artistName=artist_name).exists():
            album_obj = Album.objects.get(albumName=album_name)
            artist_obj = Artist.objects.get(artistName=artist_name)

            # check if PlaysOn Object exists
            if PlaysOn.objects.filter(FK_artistID=Artist.objects.get(artistID=artist_obj.artistID), FK_albumID_PlaysOn=album_obj.albumID).exists:
                display_str = str(album_name + " plays on " + artist_name + " Exists ")
            else:
                logger.error("Hm, both the album and the object exists, but no playedon. Something went wrong")

        else:
            # The meat of the function
            album_obj = Album.objects.create(albumName=album_name, release_date=release_date)
            artist_obj = Artist.objects.create(artistName=artist_name)
            plays_on_obj = PlaysOn.objects.create(
                FK_artistID=Artist.objects.get(artistID=artist_obj.artistID),
                FK_albumID_PlaysOn=Album.objects.get(albumID=album_obj.albumID),
                display_album_name=str(album_obj.albumName),
                display_artist_name=str(artist_obj.artistName),
                )

            # if RecordLabel exists create released object
            if RecordLabel.objects.filter(recordLabelName=record_label).exists():
                record_label_obj = RecordLabel.objects.get(recordLabelName=record_label)
                released_obj = Released.objects.create(
                    FK_albumID_Released=Album.objects.get(albumID=album_obj.albumID),
                    display_album_name=album_obj.albumName,
                    FK_recordLabelID=RecordLabel.objects.get(recordLabelID=record_label_obj.recordLabelID),
                    display_recordLabelName=record_label_obj.recordLabelName,
                    )
            # if not....
            else:
                record_label_obj = RecordLabel.objects.create(recordLabelName=record_label)
                released_obj = Released.objects.create(
                    FK_albumID_Released=Album.objects.get(albumID=album_obj.albumID),
                    display_album_name=album_obj.albumName,
                    FK_recordLabelID=RecordLabel.objects.get(recordLabelID=record_label_obj.recordLabelID),
                    display_recordLabelName=record_label_obj.recordLabelName,
                    )

            # Check if Album Art already exists
            if ImageUrl.objects.filter(url=img_url).exists():
                imageURL_obj = ImageUrl.objects.get(url=img_url)
                albumArt_obj = AlbumArt.objects.create(
                    urlID=ImageUrl.objects.get(urlID=imageURL_obj.urlID),
                    display_album_name=album_obj.albumName,
                )
                album_obj.FK_artID = AlbumArt.objects.get(artID=albumArt_obj.artID)
                album_obj.save()
            else:
                imageURL_obj = ImageUrl.objects.create(url=img_url)
                albumArt_obj = AlbumArt.objects.create(
                    urlID=ImageUrl.objects.get(urlID=imageURL_obj.urlID),
                    display_album_name=album_obj.albumName,
                )
                album_obj.FK_artID = AlbumArt.objects.get(artID=albumArt_obj.artID)
                album_obj.save()

            # For genres - iterate through the arbitrary amount of tags passed in
            if genre_tags is not None:
                for genre_name in genre_tags:
                    if Genre.objects.filter(genreName=genre_name).exists():
                        logger.debug(genre_name + " already exists")
                        genre_obj = Genre.objects.get(genreName=genre_name)
                        if Describe.objects.filter(FK_genreID=Genres.objects.get(genreID=genre_obj.genreID), FK_albumID_Describe=Album.objects.get(albumID=album_obj.albumID)).exists():
                            logger.error("Description for " + album + " and " + genre_name + " already in the system")
                        else:
                            describe_obj = Describe.objects.create(
                                FK_genreID=Genre.objects.get(genreID=genre_obj.genreID),
                                FK_albumID_Describe=Album.objects.get(albumID=album_obj.albumID),
                                display_genre_name=genre_name,
                                display_album_name=album_obj.album_name,
                            )
                    else:
                        genre_obj = Genre.objects.create(
                            genreName=genre_name
                        )
                        describe_obj = Describe.objects.create(
                                FK_genreID=Genre.objects.get(genreID=genre_obj.genreID),
                                FK_albumID_Describe=Album.objects.get(albumID=album_obj.albumID),
                                display_genre_name=genre_name,
                                display_album_name=str(album_obj.album_name),
                        )

            # Create the final userListenedTo object
            listened_to_obj = UserListenedTo.objects.create(
                user=request.user,
                FK_albumID_userLT=Album.objects.get(albumID=album_obj.albumID),
                FK_artistID=Artist.objects.get(artistID=artist_obj.artistID),
                FK_release_date_LT=album_obj.release_date,
                FK_recordLabelID_LT=RecordLabel.objects.get(recordLabelName=record_label_obj.recordLabelName),
            )
