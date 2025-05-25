from typing import TypeVar, Generic
from abc import ABC, abstractmethod

T = TypeVar('T')

class IPropertyChangedListener(Generic[T], ABC):
    @abstractmethod
    def on_property_changed(self, obj: T, property_name: str) -> None:
        ...

class IDataChanged(Generic[T], ABC):
    @abstractmethod
    def add_property_changed_listener(self, listener: IPropertyChangedListener[T]) -> None:
        ...

    @abstractmethod
    def remove_property_changed_listener(self, listener: IPropertyChangedListener[T]) -> None:
        ...

class IPropertyChangingListener(Generic[T], ABC):
    @abstractmethod
    def on_property_changing(self, obj: T, property_name: str,
                             old_value, new_value) -> bool:
        ...

class INotifyDataChanging(Generic[T], ABC):
    @abstractmethod
    def add_property_changing_listener(self, listener: IPropertyChangingListener[T]) -> None:
        ...

    @abstractmethod
    def remove_property_changing_listener(self, listener: IPropertyChangingListener[T]) -> None:
        ...

class Product(INotifyDataChanging['Product'], IDataChanged['Product']):
    def __init__(self, price: float, rate: float, availability: bool) -> None:
        self._changing_listeners: list[IPropertyChangingListener['Product']] = []
        self._changed_listeners: list[IPropertyChangedListener['Product']] = []
        self._price = price
        self._rate = rate
        self._availability = availability

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        if not isinstance(value, (int, float)):
            raise ValueError("Ошибка валидации свойства price: значение должно быть числом")
        if not self._notify_changing('price', self._price, value):
            return
        self._price = value
        self._notify_changed('price')

    @property
    def rate(self) -> float:
        return self._rate

    @rate.setter
    def rate(self, value: float) -> None:
        if not isinstance(value, (int, float)):
            raise ValueError("Ошибка валидации свойства rate: значение должно быть числом")
        if not self._notify_changing('rate', self._rate, value):
            return
        self._rate = value
        self._notify_changed('rate')

    @property
    def availability(self) -> bool:
        return self._availability

    @availability.setter
    def availability(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise ValueError("Ошибка валидации свойства availability: значение должно быть True или False")
        if not self._notify_changing('availability', self._availability, value):
            return
        self._availability = value
        self._notify_changed('availability')

    def _notify_changing(self, name: str, old, new) -> bool:
        for listener in self._changing_listeners:
            if not listener.on_property_changing(self, name, old, new):
                return False
        return True

    def _notify_changed(self, name: str) -> None:
        for listener in self._changed_listeners:
            listener.on_property_changed(self, name)

    def add_property_changing_listener(self, listener: IPropertyChangingListener['Product']) -> None:
        if listener not in self._changing_listeners:
            self._changing_listeners.append(listener)

    def remove_property_changing_listener(self, listener: IPropertyChangingListener['Product']) -> None:
        if listener in self._changing_listeners:
            self._changing_listeners.remove(listener)

    def add_property_changed_listener(self, listener: IPropertyChangedListener['Product']) -> None:
        if listener not in self._changed_listeners:
            self._changed_listeners.append(listener)

    def remove_property_changed_listener(self, listener: IPropertyChangedListener['Product']) -> None:
        if listener in self._changed_listeners:
            self._changed_listeners.remove(listener)

class ChangeLogger(IPropertyChangedListener[Product]):
    def on_property_changed(self, obj: Product, property_name: str) -> None:
        print(f"[Изменено] {property_name} у объекта {obj} -> {getattr(obj, property_name)}")

class Validator(IPropertyChangingListener[Product]):
    def on_property_changing(self, obj: Product, property_name: str, old_value, new_value) -> bool:
        if property_name == 'price' and new_value < 0:
            print("Ошибка валидации: price не может быть отрицательной")
            return False
        if property_name == 'rate' and not (0 <= new_value <= 5):
            print("Ошибка валидации: rate должен быть в диапазоне от 0 до 5")
            return False
        if property_name == 'availability' and not isinstance(new_value, bool):
            print("Ошибка валидации: availability должна быть булевым значением")
            return False
        return True

if __name__ == '__main__':
    p = Product(10.0, 3.5, True)
    logger = ChangeLogger()
    validator = Validator()
    p.add_property_changing_listener(validator)
    p.add_property_changed_listener(logger)
    p.price = 20.0
    p.rate = 6.0
    p.availability = False
    p.price = -5.0
