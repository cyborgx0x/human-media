# Generated by Django 4.2.3 on 2023-07-10 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0003_channel_channel_id_channel_lastupdate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='channel_id',
            field=models.CharField(max_length=250, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='video_id',
            field=models.CharField(max_length=250, unique=True),
        ),
    ]
