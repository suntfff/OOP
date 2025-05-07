from abc import ABC, abstractmethod

'''
регистрация и измениеине горячих клавиш
возможность отката действия и восстановление(паттерн Comand)
сохранение всех реализаций и их восстановление при перезапуске программы, реализованного классом Memento
Команды(для обычных клавиш(печатание текста))
qwerty , undo, redo:qwertyqwertqwer(ставим позицию курсора на 1 влево)
раззделяем экран на две части; в одном пишем что нажато в другой выводим результаты нажатия
'''

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass
    @abstractmethod
    def undo(self):
        pass

class Keyboard:
    def __init__(self, snapshot_maker):
        self.snapshot_maker = snapshot_maker

    def register(self, combination:str, command: Command):
        pass

    def undo(self):
        '''
        1. Найти последнюю запущенную команду в истории
        2. Выполнить для нее undo
        3. Запоминаем позицию
        '''

    def redo(self):
        pass