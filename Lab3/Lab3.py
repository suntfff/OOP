from abc import ABC, abstractmethod
import os, socket, re, logging, platform, sys, win32evtlogutil, win32evtlog, logging, logging.handlers


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

    def handle(self, text: str) -> None:
        base_dir = os.path.dirname(__file__)
        self._file_path = os.path.join(base_dir, self._file_path)
        try:
            with open(self._file_path, 'a', encoding='utf-8') as f:
                f.write(text + '\n')
        except PermissionError:
            raise PermissionError(f"Нет доступа к файлу {self._file_path}")
        except OSError as error:
            raise OSError(f"Ошибка {error} при открытии файла {self._file_path}")

class SocketHandler(ILogHandler):
    def __init__(self, host: str, port: int) -> None:
        self._host = host
        self._port = port

    def handle(self, text: str) -> None:
        try:
            with socket.create_connection((self._host, self._port), 15) as s:
                s.sendall(text.encode('utf-8'))
        except socket.timeout as err:
            raise socket.timeout(f'Превышено время ожидания: {err}') from err
        except socket.error as err:
            raise socket.error(f"Ошибка при отправке логов на {self._host}:{self._port}: {err}") from err

class SyslogHandler(ILogHandler):
    def __init__(self,
                 address: tuple[str, int] = ('localhost', 514),
                 facility: int = logging.handlers.SysLogHandler.LOG_USER) -> None:
        self._handler = logging.handlers.SysLogHandler(address, facility)
        fmt = logging.Formatter('%(message)s')
        self._handler.setFormatter(fmt)

    def handle(self, text: str) -> None:
        record = logging.LogRecord(
            name='SyslogHandler',
            level=logging.INFO,
            pathname='', lineno=0,
            msg=text, args=(), exc_info=None
        )
        try:
            self._handler.emit(record)
        except Exception as err:
            raise OSError(f"Ошибка при отправке в syslog ({self._handler.address}): {err}") from err

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



