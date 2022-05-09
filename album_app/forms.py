from django import forms
from .models import *


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['albumName', 'release_date']
        labels = {
            'albumName': 'Name of Album'
        }


class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['artistName']
        labels = {
            'artistName': 'Name of Artist'
        }


class PlaysOnForm(forms.ModelForm):
    class Meta:
        model = PlaysOn
        fields = ['FK_artistID', 'FK_albumID_PlaysOn']


class ImageURLForm(forms.ModelForm):
    class Meta:
        model = ImageUrl
        fields = ['url']
        labels = {
            'url': 'Album Art image URL'
        }


class RecordLabelForm(forms.ModelForm):
    class Meta:
        model = RecordLabel
        fields = ['recordLabelName']


class ReleasedForm(forms.ModelForm):
    class Meta:
        model = Released
        fields = ['display_recordLabelName']
        labels = {
                'display_recordLabelName': 'Record Label'
        }


class GenreForm (forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['genreName']


class DescribeForm(forms.ModelForm):
    class Meta:
        model = Describe
        fields = ['display_genre_name']


class BandcampForm(forms.ModelForm):
    class Meta:
        model = BandcampUserName
        fields = ['bc_username']


class UserListenedToForm(forms.ModelForm):
    class Meta:
        model = UserListenedTo
        fields = ['FK_ratingLT', 'relisten', 'comment']
        labels = {
                'FK_ratingLT': "Your rating",
                'relisten': "Do you want to relisten?",
                'comment': "Your comments",
                }


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['category', 'feedback_text']
        labels = {
                'feedback_text': '',
                'category': '',
                }
