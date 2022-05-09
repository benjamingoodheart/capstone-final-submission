# Django dependencies
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist

# Stdlib
from tokenize import Name
import uuid
import secrets
import datetime


# Constant Declaration
RELISTEN_CHOICES = (
    (True, "YES"),
    (False, "NO")
    )
DEFAULT_DATE = '2022-01-01'
FEEDBACK_CHOICES = (
    ('BUG', 'Bug'),
    ('DESIGN', 'Design'),
    ('SUGGESTION', 'Suggestion'),
    ('MISC', 'Misc'),
)


# Models
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hasSpotify = models.BooleanField(default=False)
    spotifyAccessToken = models.CharField(max_length=500, blank=True, null=True)
    spotifyRefreshToken = models.CharField(max_length=500, blank=True, null=True)
    hasApple = models.BooleanField(default=False)
    bandcampUserName = models.CharField(max_length=100, blank=True)


@receiver(post_save, sender=User)
def createUserProfile(sender, instance, created, **kwargs):
    try:
        instance.profile.save()
    except ObjectDoesNotExist:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def saveUserProfile(sender, instance, **kwargs):
    instance.profile.save()


class Artist(models.Model):
    artistID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artistName = models.CharField(max_length=300, unique=True)

    def __str__(self):
        return self.artistName


class Album(models.Model):
    albumID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    albumName = models.CharField(max_length=300)
    release_date = models.DateField(default=datetime.date(2022, 1, 1))
    FK_artID = models.ForeignKey('AlbumArt', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.albumName


class AlbumArt(models.Model):
    artID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    urlID = models.ForeignKey('ImageUrl', on_delete=models.CASCADE)
    display_album_name = models.CharField(max_length=300, null=True)

    class Meta:
        verbose_name_plural = "Album Art"

    def __str__(self):
        if self.display_album_name is None:
            self.display_album_name = "Artist"
        return self.display_album_name


class ImageUrl(models.Model):
    urlID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.URLField(max_length=200, default="https://upload.wikimedia.org/wikipedia/commons/2/27/Red_square.svg")

    def __str__(self):
        return self.url


class PlaysOn(models.Model):
    FK_artistID = models.ForeignKey('Artist', on_delete=models.CASCADE)
    display_album_name = models.CharField(max_length=300, null=True, blank=True)
    FK_albumID_PlaysOn = models.ForeignKey('Album', on_delete=models.CASCADE)
    display_artist_name = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        if self.display_artist_name is None:
            self.display_artist_name = "Artist"
        if self.display_album_name is None:
            self.display_album_name = "Album"
        display_str = str(self.display_artist_name) + " plays On " + str(self.display_album_name)
        return display_str


class RecordLabel(models.Model):
    recordLabelID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recordLabelName = models.CharField(max_length=200, unique=True, null=True)

    def __str__(self):
        return self.recordLabelName


class Released(models.Model):
    releasedID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    FK_recordLabelID = models.ForeignKey('RecordLabel', on_delete=models.CASCADE, null=True)
    display_recordLabelName = models.CharField(max_length=100, null=True, blank=True, default="Self-Released")
    FK_albumID_Released = models.ForeignKey('Album', on_delete=models.CASCADE, null=True)
    display_album_name = models.CharField(max_length=300, null=True, blank=True, default="Album Name")

    class Meta:
        verbose_name_plural = "Releases"

    def __str__(self):
        display_str = str(self.display_recordLabelName) + " Released " + str(self.display_album_name)
        return display_str


class Genre(models.Model):
    genreID = models.UUIDField(primary_key=True, default=uuid.uuid4)
    genreName = models.CharField(max_length=100, null=True, unique=True)

    def __str__(self):
        return str(self.genreName)


class Describe(models.Model):
    describeID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    FK_albumID_Describe = models.ForeignKey('Album', on_delete=models.CASCADE, null=True)
    display_album_name = models.CharField(max_length=300, default="Album Name")
    FK_genreID = models.ForeignKey('Genre', on_delete=models.CASCADE, null=True)
    display_genre_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        display_str = str(self.display_genre_name) + " describes " + str(self.display_album_name)
        return str(display_str)


class UserListenedTo(models.Model):
    ultID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    FK_albumID_userLT = models.ForeignKey('Album', on_delete=models.CASCADE)
    FK_artistID = models.ForeignKey('Artist', on_delete=models.CASCADE)  # TODO: RENAME THIS to FK_artistID_LT
    FK_release_date_LT = models.DateField(default=DEFAULT_DATE)
    FK_recordLabelID_LT = models.ForeignKey('RecordLabel', on_delete=models.CASCADE, null=True)
    FK_ratingLT = models.DecimalField(max_digits=5, decimal_places=1, default=7.5)
    relisten = models.BooleanField(choices=RELISTEN_CHOICES, default=False)
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        display_str = str(self.user) + " has listened to " + str(self.FK_albumID_userLT)
        return str(display_str)

    def get_absolute_url(self):
        return reverse('detailView', args=[str(self.ultID)])


class BandcampUserName(models.Model):
    bc_username = models.CharField(max_length=100, default="Not Set")
    FK_user_bc_scraper = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # # TODO: Rename this if you can

    def __str__(self):
        return self.bc_username


class Feedback(models.Model):
    feedback_ticket_num = models.AutoField(primary_key=True)
    made_by = models.ForeignKey(User, on_delete=models.CASCADE)
    made_on = models.DateTimeField(auto_now=True)
    feedback_text = models.TextField()
    category = models.CharField(choices=FEEDBACK_CHOICES, max_length=50, default="Bug")
