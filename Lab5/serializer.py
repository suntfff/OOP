from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Sequence, List, Type
import json
import os
from dataclasses import is_dataclass, fields, asdict

T = TypeVar('T')

class ISerializer(ABC, Generic[T]):
    @abstractmethod
    def save(self, data: Sequence[T], filename: str) -> None:
        ...

    @abstractmethod
    def load(self, filename: str) -> List[T]:
        ...

class IDataclassSerializer(ISerializer[T], ABC):
    @abstractmethod
    def save(self, data: Sequence[T], filename: str) -> None:
        ...

    @abstractmethod
    def load(self, filename: str) -> List[T]:
        ...

class DataclassJsonSerializer(IDataclassSerializer[T], Generic[T]):
    def __init__(self, cls: Type[T]):
        if not is_dataclass(cls):
            raise TypeError(f"Класс {cls.__name__} не является dataclass.")
        self._cls = cls

    def save(self, data: Sequence[T], filename: str) -> None:
        try:
            os.makedirs(os.path.dirname(filename) or '.', exist_ok=True)
            serialized = [
                {k: v for k, v in asdict(item).items() if k != "password"}
                for item in data
            ]
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(serialized, f, indent=2, ensure_ascii=False)
        except PermissionError:
            raise PermissionError(f"Нет прав для записи в файл: {filename}")
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл не найден: {filename}")
        except Exception as e:
            raise IOError(f"Ошибка при сохранении данных в файл '{filename}': {e}")

    def load(self, filename: str) -> List[T]:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                raw = json.load(f)
            cls_fields = {f.name for f in fields(self._cls)}
            result = []
            for item in raw:
                filtered = {k: v for k, v in item.items() if k in cls_fields}
                result.append(self._cls(**filtered))
            return result
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            raise ValueError(f"Файл '{filename}' повреждён или содержит некорректный JSON.")
        except Exception as e:
            raise IOError(f"Ошибка при загрузке данных из файла '{filename}': {e}")

