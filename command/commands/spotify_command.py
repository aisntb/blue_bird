from irispy2 import ChatContext

class SpotifyCommand:
    invoke = "spotify"
    help = "!spotify 노래검색"
    type = "kl"

    def handle(self, event:ChatContext, kl):
        event.reply("노래검색중입니다.")

