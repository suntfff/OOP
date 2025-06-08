from system_controller import SystemController
from commands import Command, CommandFactory, Binding

class VirtualKeyboard:
    def __init__(self, system_controller: SystemController):
        self.system_controller = system_controller
        self.bindings: dict[str, Binding] = {}
        self.undo_stack: list[Command] = []
        self.redo_stack: list[Command] = []

    def bind(self, key: str, type_: str, params: dict):
        self.bindings[key] = Binding(key, type_, params)

    def press(self, key: str):
        b = self.bindings.get(key)
        if not b: return
        cmd = CommandFactory.create(b.type, b.params, self.system_controller)
        cmd.execute()
        self.undo_stack.append(cmd)
        self.redo_stack.clear()

    def undo(self):
        if not self.undo_stack: return
        cmd = self.undo_stack.pop()
        cmd.undo()
        self.redo_stack.append(cmd)

    def redo(self):
        if not self.redo_stack: return
        cmd = self.redo_stack.pop()
        cmd.execute()
        self.undo_stack.append(cmd)