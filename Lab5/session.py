import os
import json
from abc import ABC, abstractmethod
from typing import Optional, TypeVar, Generic
from dataclasses import dataclass

@dataclass
class Session:
    login: str

T = TypeVar('T')

class IDataSerializer(ABC, Generic[T]):
    @abstractmethod
    def serialize(self, item: T) -> bytes:
        ...

    @abstractmethod
    def deserialize(self, data: bytes) -> T:
        ...

class JsonSessionSerializer(IDataSerializer[Session]):
    def serialize(self, session: Session) -> bytes:
        try:
            return json.dumps(session.__dict__).encode()
        except Exception as e:
            raise ValueError(f"Ошибка сериализации сессии: {e}")

    def deserialize(self, data: bytes) -> Session:
        try:
            return Session(**json.loads(data.decode()))
        except json.JSONDecodeError:
            raise ValueError("Ошибка декодирования JSON при загрузке сессии.")
        except Exception as e:
            raise ValueError(f"Ошибка десериализации сессии: {e}")

class SessionStorage:
    def __init__(self, path: str, serializer: IDataSerializer[Session]):
        self.path = path
        self.serializer = serializer

    def save(self, session: Session) -> None:
        try:
            with open(self.path, 'wb') as f:
                f.write(self.serializer.serialize(session))
        except PermissionError:
            raise PermissionError(f"Нет прав для записи файла: {self.path}")
        except Exception as e:
            raise IOError(f"Ошибка при сохранении сессии: {e}")

    def load(self) -> Optional[Session]:
        try:
            with open(self.path, 'rb') as f:
                return self.serializer.deserialize(f.read())
        except FileNotFoundError:
            return None
        except Exception as e:
            raise IOError(f"Ошибка при загрузке сессии: {e}")

    def clear(self) -> None:
        try:
            os.remove(self.path)
        except FileNotFoundError:
            pass
        except PermissionError:
            raise PermissionError(f"Нет прав для удаления файла: {self.path}")
        except Exception as e:
            raise IOError(f"Ошибка при удалении файла сессии: {e}")

