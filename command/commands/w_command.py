from utils.menu_utils import move_up
from irispy2 import ChatContext

class WCommand:
    invoke = "w"
    help = ""
    type = "text"

    def handle(self, event:ChatContext, kl):
        content = event.message.msg[len("!"):].strip()
        count = len(content) - len(content.lstrip('w'))
        move_up(event, count)

