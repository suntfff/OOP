from Lab5.serializer import IDataclassSerializer
from keyboard import VirtualKeyboard
from commands import Binding

class KeyboardStateSaver:
    def __init__(self, serializer: IDataclassSerializer[Binding]):
        self._serializer = serializer

    def save(self, keyboard: VirtualKeyboard, filename: str):
        self._serializer.save(list(keyboard.bindings.values()), filename)

    def load(self, keyboard: VirtualKeyboard, filename: str):
        for b in self._serializer.load(filename):
            keyboard.bind(b.key, b.type, b.params)