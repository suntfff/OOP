from abc import ABC, abstractmethod
import os, re


class ILogHandler(ABC):
    @abstractmethod
    def handle(self, text: str) -> None:
        pass

class ConsoleLogHandler(ILogHandler):
    def handle(self, text: str) -> None:
        print(text)

class FileLogHandler(ILogHandler):
    def __init__(self, file_path: str) -> None:
        self._file_path = file_path
        base_dir = os.path.dirname(__file__)
        self._file_path = os.path.join(base_dir, self._file_path)

    def handle(self, text: str) -> None:
        try:
            with open(self._file_path, 'a', encoding='utf-8') as f:
                f.write(text + '\n')
        except PermissionError:
            raise PermissionError(f"Нет доступа к файлу {self._file_path}")
        except OSError as error:
            raise OSError(f"Ошибка {error} при открытии файла {self._file_path}")

class SocketHandler(ILogHandler):
    def handle(self, text: str) -> None:
        print('Запись в сокет')

class SyslogHandler(ILogHandler):
    def handle(self, text: str) -> None:
        print('Заипсь в системный лог')

class ILogFilter(ABC):
    @abstractmethod
    def match(self, text: str) -> bool:
        pass

class SimpleLogFilter(ILogFilter):
    def __init__(self, pattern: str) -> None:
        self._pattern = pattern

    def match(self, text: str) -> bool:
        return self._pattern in text

class ReLogFilter(ILogFilter):
    def __init__(self, pattern: str) -> None:
        self._pattern = pattern

    def match(self, text: str) -> bool:
        return bool(re.search(self._pattern, text))

class Logger:
    def __init__(self, handlers: list[ILogHandler],
                 filters: list[ILogFilter]) -> None:
        self._handlers = handlers
        self._filters = filters

    def log(self, text: str) -> None:
        if not all(log_filter.match(text) for log_filter in self._filters):
            return None

        for handler in self._handlers:
            handler.handle(text)





