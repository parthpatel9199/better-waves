import os
from pathlib import Path

from django.core.files import File
from eyed3 import id3
from BetterWaves import settings
from music import models

from music.logger_labeler import logger
print = logger(__name__.split('.')[-1])


def load_library():
    files = []
    library_path = os.path.join(settings.MEDIA_ROOT, 'music')
    entries = Path(library_path)
    for entry in entries.iterdir():
        files.append(entry)

    tag = id3.Tag()

    for file in files:
        # Parse the file
        filepath = os.path.join('music', file.name)
        tag.parse(os.path.join(library_path, file.name))

        # Delete if any of tags is None
        if not (tag.title and tag.artist and tag.album and tag.genre):

            os.remove(filepath)
            continue

        # Create Artist model and check if already exists
        artist = models.Artist(title=tag.artist)
        dup_artist = models.Artist.objects.filter(title=tag.artist)
        if not dup_artist:
            # print('Artist added:', tag.artist)
            artist.save()
        else:
            # print('dup_artists found:', len(dup_artist))
            artist = dup_artist[0]

        # Create Album model and check if already exists
        album = models.Album(title=tag.album, artist=artist)
        dup_album = models.Album.objects.filter(title=tag.album)
        if not dup_album:
            # print('Album added:', tag.album)
            album.save()
        else:
            # print('dup_album found:', len(dup_album))
            album = dup_album[0]

        # Create Song model and check if already exists
        dup_song = models.Song.objects.filter(title=tag.title, album=album)
        if not dup_song:
            s = models.Song(title=tag.title, album=album, genre=tag.genre.name, file=filepath)
            print('Song added:', file.name)
            s.save()

    print()
    print("-="*10 + " LOAD COMPLETE " + '=-'*10)
    print()
