from irispy2 import ChatContext

from kakaolink import IKakaoLinkCookieStorage, IKakaoLinkAuthorizationProvider, KakaoLink


class SpotifyCommand:
    invoke = "상점"
    help = "상점 메뉴를 불러옵니다."

    def handle(self, event:ChatContext, kl):
        event.reply("노래검색중입니다.")

