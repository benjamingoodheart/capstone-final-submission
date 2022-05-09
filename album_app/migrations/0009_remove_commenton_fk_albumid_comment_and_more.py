# Generated by Django 4.0.2 on 2022-04-19 01:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('album_app', '0008_alter_userlistenedto_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commenton',
            name='FK_albumID_Comment',
        ),
        migrations.RemoveField(
            model_name='commenton',
            name='FK_commentID',
        ),
        migrations.RemoveField(
            model_name='rating',
            name='FK_albumID_rating',
        ),
        migrations.RemoveField(
            model_name='rating',
            name='ratingUserName',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='CommentOn',
        ),
        migrations.DeleteModel(
            name='Rating',
        ),
    ]