from abc import ABC, abstractmethod
from system_controller import SystemController
from dataclasses import dataclass

@dataclass
class Binding:
    key: str
    type: str
    params: dict

class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        ...

    @abstractmethod
    def undo(self)  -> None:
        ...

    @abstractmethod
    def get_type(self) -> str:
        ...

    @abstractmethod
    def get_params(self) -> dict:
        ...


class VolumeUpCommand(Command):
    def __init__(self, system_controller : SystemController, step: int = 20)  -> None:
        self.system_controller = system_controller
        self.step = step

    def execute(self) -> None:
        self.system_controller.volume = min(100, self.system_controller.volume + self.step)
        self.system_controller.log(f'volume increased +{self.step}%')

    def undo(self) -> None:
        self.system_controller.volume = max(0, self.system_controller.volume - self.step)
        self.system_controller.log(f'volume decreased +{self.step}%')

    def get_type(self) -> str:
        return 'VolumeUp'

    def get_params(self) -> dict:
        return {'step': self.step}


class VolumeDownCommand(Command):
    def __init__(self, system_controller: SystemController, step: int = 20) -> None:
        self.system_controller = system_controller
        self.step = step

    def execute(self) -> None:
        self.system_controller.volume = max(0, self.system_controller.volume - self.step)
        self.system_controller.log(f'volume decreased +{self.step}%')

    def undo(self) -> None:
        self.system_controller.volume = min(100, self.system_controller.volume + self.step)
        self.system_controller.log(f'volume increased +{self.step}%')

    def get_type(self) -> str:
        return 'VolumeDown'

    def get_params(self) -> dict:
        return {'step': self.step}


class MediaPlayerCommand(Command):
    def __init__(self, system_controller: SystemController) -> None:
        self.system_controller = system_controller
        self.previous = None

    def execute(self) -> None:
        self.previous = self.system_controller.media_playing
        self.system_controller.media_playing = not self.previous
        self.system_controller.log('media player launched' if self.system_controller.media_playing else 'media player closed')

    def undo(self) -> None:
        if self.previous is None: return
        self.system_controller.media_playing = self.previous
        self.system_controller.log('media player launched' if self.system_controller.media_playing else 'media player closed')

    def get_type(self) -> str:
        return 'MediaPlayer'

    def get_params(self) -> dict:
        return {}


class KeyCommand(Command):
    def __init__(self, system_controller: SystemController, char: str) -> None:
        self.system_controller = system_controller
        self.char = char
        self.prev = ''

    def execute(self) -> None:
        self.prev = self.system_controller.text
        self.system_controller.text += self.char
        self.system_controller.log(self.system_controller.text)

    def undo(self) -> None:
        self.system_controller.text = self.prev
        self.system_controller.log(self.system_controller.text)

    def get_type(self) -> str:
        return 'Key'

    def get_params(self) -> dict:
        return {'char': self.char}

class CommandFactory:
    @staticmethod
    def create(type: str, params: dict, system_controller: SystemController) -> Command:
        if type == 'VolumeUp': return VolumeUpCommand(system_controller, params.get('step', 20))
        if type == 'VolumeDown': return VolumeDownCommand(system_controller, params.get('step', 20))
        if type == 'MediaPlayer': return MediaPlayerCommand(system_controller)
        if type == 'Key': return KeyCommand(system_controller, params.get('char', ''))
        raise ValueError(type)