from irispy2 import ChatContext

from kakaolink import IKakaoLinkCookieStorage, IKakaoLinkAuthorizationProvider, KakaoLink
from utils.menu_utils import add_user

items = [
    "귀고리", "눈장식", "망토", "모자", "무기", "방패",
    "상의", "성형", "신발", "얼굴장식", "장갑", "피부",
    "하의", "한벌옷", "헤어"
]

class StoreCommand:
    invoke = "상점"
    help = "상점 메뉴를 불러옵니다."
    type = "text"

    def handle(self, event:ChatContext):
        result = "\n".join(f"{i+1}. {item}" for i, item in enumerate(items))
        event.reply("상점입니다. 원하는 번호를 선택해주세요.\n\n"+result)
        add_user(event.sender.id)

