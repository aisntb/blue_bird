import random

from iris import ChatContext

class KermitCommand:
    invoke = "커밋"
    help = "!커밋 으로 랜덤한 커밋 개구리 사진을 가져옵니다."
    type = "kl"

    def handle(self, event:ChatContext, kl):
        random_number = random.randint(1, 33)
        url = f"https://studybot.s3.ap-northeast-2.amazonaws.com/kermit/{random_number}.jpg"
        kl.send(
            receiver_name=event.room.name,
            template_id=15476,
            template_args={
                "${TH_IMAGE_URL_0}": url
            },
        )


