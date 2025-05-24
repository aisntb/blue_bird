from irispy2 import ChatContext
from utils.menu_utils import go_back

class ACommand:
    invoke = "a"
    help = ""
    type = "text"

    def handle(self, event:ChatContext, kl):
        go_back(event)

