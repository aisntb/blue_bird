from irispy2 import ChatContext
from utils.spotify import search_track

class SpotifyCommand:
    invoke = "spotify"
    help = "!spotify 노래검색"
    type = "kl"

    def handle(self, event:ChatContext, kl):
        title = event.message.msg[len(">spotify "):].strip()
        result = search_track(title)
        track = result[0]
        track_id = track['id']
        album_art_url = track['album']['images'][0]['url']
        track_name = track['name']
        artist_name = track['artists'][0]['name']
        kl.send(
                receiver_name=event.room.name,
                template_id=15476,
                template_args={
                    "${TH_IMAGE_URL_0}": album_art_url,
                    "${TITLE}":track_name,
                    "${DESC}":artist_name,
                    "URL":"https://naver.com",
                    "${SHARED_FROM}":f"spotify:track:{track_id}"
                },
            )

