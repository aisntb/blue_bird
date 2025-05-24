import re
from typing import Dict

from irispy2 import ChatContext

from command.commands import ICommand
from command.commands.a_command import ACommand
from command.commands.d_command import DCommand
from command.commands.s_command import SCommand
from command.commands.select_command import SelectCommand
from command.commands.spotify_command import SpotifyCommand
from command.commands.w_command import WCommand
from command.commands.weather_command import WeatherCommand



class CommandManager:
    def __init__(self):
        self.exact_commands: Dict[str, ICommand] = {}
        print("Loading commands...")
        self.add_command(SpotifyCommand())
        self.add_command(WeatherCommand())
        self.add_command(WCommand())
        self.add_command(ACommand())
        self.add_command(SCommand())
        self.add_command(DCommand())
        self.add_command(SelectCommand())

    def add_command(self, command: ICommand):
        self.exact_commands[command.invoke] = command
        print(f"☀️ 명령어 등록: {command.invoke}")

    def handle_command(self, event: ChatContext, kl):
        print(f"[메세지] {event.sender.name}: {event.message.msg}")
        prefix = "!"
        if not event.message.msg.startswith(prefix):
            return

        content = event.message.msg[len(prefix):]
        split = content.split()
        if not split:
            return

        invoke = split[0]
        command = self.exact_commands.get(invoke)
        msg = event.message.msg
        match = re.fullmatch(r"!([wasd])\1*", msg)  # !w, !ww, !aaa 등 매치됨

        if match:
            key = match.group(1)  # "w", "a", "s", "d" 중 하나
            command = self.exact_commands.get(key)
            command.handle(event, kl)
        elif command and command.type == "kl":
            command.handle(event, kl)
        elif command:
            command.handle(event)