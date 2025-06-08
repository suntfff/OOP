from Lab3.Lab3 import Logger, ConsoleLogHandler, FileLogHandler, SimpleLogFilter
from Lab5.serializer import DataclassJsonSerializer
from system_controller import SystemController
from keyboard import VirtualKeyboard
from state_saver import KeyboardStateSaver, Binding

def main() -> None:
    handlers = [ConsoleLogHandler(), FileLogHandler('keyboard_logger.txt')]
    filters = [SimpleLogFilter('')]
    logger = Logger(handlers, filters)
    system_controller = SystemController(logger)
    keyboard = VirtualKeyboard(system_controller)
    saver = KeyboardStateSaver(DataclassJsonSerializer(Binding))
    keyboard.bind('a', 'Key', {'char': 'a'})
    keyboard.bind('b', 'Key', {'char': 'b'})
    keyboard.bind('c', 'Key', {'char': 'c'})
    keyboard.bind('ctrl++', 'VolumeUp', {'step': 20})
    keyboard.bind('ctrl+-', 'VolumeDown', {'step': 20})
    keyboard.bind('ctrl+p', 'MediaPlayer', {})
    keyboard.press('a')
    keyboard.press('b')
    keyboard.press('c')
    keyboard.undo()
    keyboard.undo()
    keyboard.redo()
    keyboard.press('ctrl++')
    keyboard.press('ctrl+-')
    keyboard.press('ctrl+p')
    keyboard.undo()
    keyboard.press('d')
    keyboard.undo()
    keyboard.undo()
    saver.save(keyboard, 'keyboard_info.json')

if __name__ == '__main__':
    main()