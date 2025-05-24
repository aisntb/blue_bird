from irispy2 import ChatContext

from utils.menu_utils import confirm


class SelectCommand:
    invoke = "선택"
    help = "!선택 <번호>"
    type = "kl"

    def handle(self, event:ChatContext, kl):
        confirm(event, kl)

