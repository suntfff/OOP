from user import PasswordRecord, User
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Sequence, Optional, List, Type
from dataclasses import is_dataclass, asdict, fields
import os
import json

T = TypeVar('T')

class IDataRepository(ABC, Generic[T]):
    @abstractmethod
    def get_all(self) -> Sequence[T]:
        ...

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[T]:
        ...

    @abstractmethod
    def add(self, item: T) -> None:
        ...

    @abstractmethod
    def update(self, item: T) -> None:
        ...

    @abstractmethod
    def delete(self, item: T) -> None:
        ...

class IUserRepository(IDataRepository["User"], ABC):
    @abstractmethod
    def get_by_login(self, login: str) -> Optional["User"]:
        ...

class IDataclassSerializer(ABC, Generic[T]):
    @abstractmethod
    def save(self, data: Sequence[T], filename: str) -> None:
        ...

    @abstractmethod
    def load(self, filename: str) -> List[T]:
        ...

class DataclassJsonSerializer(IDataclassSerializer[T]):
    def __init__(self, cls: Type[T]):
        if not is_dataclass(cls):
            raise TypeError(f"{cls.__name__} не является dataclass")
        self._cls = cls

    def save(self, data: Sequence[T], filename: str) -> None:
        try:
            os.makedirs(os.path.dirname(filename) or '.', exist_ok=True)
            to_dump = [asdict(item) for item in data]
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(to_dump, f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise IOError(f"Ошибка при сохранении файла '{filename}': {e}")

    def load(self, filename: str) -> List[T]:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                raw = json.load(f)
            cls_fields = {f.name for f in fields(self._cls)}
            result = []
            for item_dict in raw:
                filtered = {k: v for k, v in item_dict.items() if k in cls_fields}
                result.append(self._cls(**filtered))
            return result
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            raise ValueError(f"Файл '{filename}' повреждён или содержит некорректный JSON.")
        except Exception as e:
            raise IOError(f"Ошибка при загрузке файла '{filename}': {e}")

class DataRepository(IDataRepository[T], Generic[T]):
    def __init__(self, serializer: IDataclassSerializer[T], filename: str):
        self.serializer = serializer
        self.filename = filename
        try:
            self._data = self.serializer.load(self.filename)
        except Exception as e:
            print(f"Ошибка загрузки данных из '{self.filename}': {e}")
            self._data = []

    def _save(self):
        try:
            self.serializer.save(self._data, self.filename)
        except Exception as e:
            raise IOError(f"Ошибка при сохранении данных: {e}")

    def get_all(self) -> Sequence[T]:
        return list(self._data)

    def get_by_id(self, id: int) -> Optional[T]:
        return next((item for item in self._data if getattr(item, 'id', None) == id), None)

    def add(self, item: T) -> None:
        try:
            self._data.append(item)
            self._save()
        except Exception as e:
            raise RuntimeError(f"Ошибка при добавлении элемента: {e}")

    def update(self, item: T) -> None:
        item_id = getattr(item, 'id', None)
        if item_id is None:
            raise ValueError("Обновляемый объект не имеет поля 'id'")
        for i, existing in enumerate(self._data):
            if getattr(existing, 'id', None) == item_id:
                self._data[i] = item
                self._save()
                return
        raise ValueError(f"Элемент с id={item_id} не найден для обновления")

    def delete(self, item: T) -> None:
        item_id = getattr(item, 'id', None)
        if item_id is None:
            raise ValueError("Удаляемый объект не имеет поля 'id'")
        new_list = [d for d in self._data if getattr(d, 'id', None) != item_id]
        if len(new_list) == len(self._data):
            raise ValueError(f"Элемент с id={item_id} не найден для удаления")
        self._data = new_list
        self._save()

class UserRepository(DataRepository["User"], IUserRepository):
    def get_by_login(self, login: str) -> Optional["User"]:
        try:
            return next((u for u in self._data if u.login == login), None)
        except Exception as e:
            print(f"Ошибка при поиске пользователя по логину: {e}")
            return None

class PasswordRepository(DataRepository[PasswordRecord]):
    def get_by_login(self, login: str) -> Optional[PasswordRecord]:
        try:
            return next((p for p in self._data if p.login == login), None)
        except Exception as e:
            print(f"Ошибка при поиске пароля по логину: {e}")
            return None

    def add(self, item: PasswordRecord) -> None:
        try:
            existing = self.get_by_login(item.login)
            if existing:
                existing.password_hash = item.password_hash
                self._save()
            else:
                super().add(item)
        except Exception as e:
            raise RuntimeError(f"Ошибка при добавлении записи пароля: {e}")

