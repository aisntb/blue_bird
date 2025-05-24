from utils.menu_utils import move_down
from irispy2 import ChatContext

class SCommand:
    invoke = "s"
    help = ""
    type = "text"

    def handle(self, event:ChatContext, kl):
        content = event.message.msg[len("!"):].strip()
        count = len(content) - len(content.lstrip('s'))
        move_down(event, count)

