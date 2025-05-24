from irispy2 import ChatContext
from utils.menu_utils import confirm

class DCommand:
    invoke = "d"
    help = ""
    type = "kl"

    def handle(self, event:ChatContext, kl):
        confirm(event, kl)