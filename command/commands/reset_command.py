from irispy2 import ChatContext

from utils.menu_utils import inventory, reset_inventory
from utils.spotify import search_track
from utils.store_gui import get_avatar, get_avatar_img


class ResetCommand:
    invoke = "초기화"
    help = "아바타 착장을 초기화합니다."
    type = "kl"

    def handle(self, event:ChatContext, kl):
        user_id = str(event.sender.id)
        reset_inventory(user_id)
        code = get_avatar(inventory[user_id])
        img = get_avatar_img(code)
        kl.send(
            receiver_name=event.room.name,
            template_id=15476,
            template_args={
                "${TH_IMAGE_URL_0}": img
            },
        )

