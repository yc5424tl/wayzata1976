from django.core.management.base import BaseCommand
from ...models import Song
import json
from django.conf import settings

from django.templatetags.static import static

class Command(BaseCommand):
    help = "Instantiates Song objects from target JSON file"

    def handle(self, *args, **kwargs):
        json_file = "wayzata76_web/static/json/songs.json"
        with open(json_file) as songs_json:
            json_data = json.load(songs_json)
            for record in json_data:
                position=record['position']
                name=record['single']
                artist=record['artist']
                peak=record['peak']
                weeks_peak=record['weeks_peak']
                weeks_top10 = record['weeks_10']
                weeks_top40 = record['weeks_40']

                new_song = Song(
                    position=position,
                    name=name,
                    artist=artist,
                    peak=peak,
                    weeks_peak=weeks_peak,
                    weeks_top10=weeks_top10,
                    weeks_top40=weeks_top40
                )
                new_song.get_video_id()
                new_song.get_url()
                new_song.save()
        print('Songs Loaded')
        return
                
