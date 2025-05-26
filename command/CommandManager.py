import re
from typing import Dict

from irispy2 import ChatContext

from command.commands import ICommand
from command.commands.ai_command import AiCommand
from command.commands.avartar_command import AvatarCommand
from command.commands.eval_command import EvalCommand
from command.commands.kermit_command import KermitCommand
from command.commands.reset_command import ResetCommand
from command.commands.spotify_command import SpotifyCommand
from command.commands.store_command import StoreCommand
from command.commands.weather_command import WeatherCommand
from utils.menu_utils import cleanup_users, handle_user_input


class CommandManager:
    def __init__(self):
        self.exact_commands: Dict[str, ICommand] = {}
        print("Loading commands...")
        self.add_command(SpotifyCommand())
        self.add_command(WeatherCommand())
        self.add_command(KermitCommand())
        self.add_command(EvalCommand())
        self.add_command(AiCommand())
        self.add_command(StoreCommand())
        self.add_command(ResetCommand())
        self.add_command(AvatarCommand())

    def add_command(self, command: ICommand):
        self.exact_commands[command.invoke] = command
        print(f"☀️ 명령어 등록: {command.invoke}")

    def handle_command(self, event: ChatContext, kl):
        print(f"[메세지] {event.sender.name}: {event.message.msg}")
        prefix = ">"
        pattern = r"^\d+$"
        is_number = re.fullmatch(pattern, event.message.msg)
        if is_number:
            result = handle_user_input(event, kl)


        if not event.message.msg.startswith(prefix):
            return

        content = event.message.msg[len(prefix):]
        split = content.split()
        if not split:
            return

        invoke = split[0]
        command = self.exact_commands.get(invoke)
        msg = event.message.msg
        match = re.fullmatch(r">([wasd])\1*", msg)  # !w, !ww, !aaa 등 매치됨

        if match:
            key = match.group(1)  # "w", "a", "s", "d" 중 하나
            command = self.exact_commands.get(key)
            command.handle(event, kl)
        elif command and command.type == "kl":
            command.handle(event, kl)
        elif command:
            command.handle(event)
        cleanup_users()