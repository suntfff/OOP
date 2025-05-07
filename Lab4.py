from abc import ABC, abstractmethod
from typing import TypeVar, Protocol

T = TypeVar('T')

class PropertyChangedListenerProtocol(Protocol):
    def on_property_changed(self, obj: T, property_name) -> None:
        pass

class DataChangedProtocol(Protocol):
    def add_property_changed_listener(self,
        listener: PropertyChangedListenerProtocol):
        pass

    def remove_property_changed_listener(self,
        listener: PropertyChangedListenerProtocol):
        pass

class PropertyChangingListenerProtocol(Protocol):
    def on_property_changing(self, obj: T, property_name, old_value,
                             new_value) -> bool:
        pass

class DataChangingProtocol(Protocol):
    def add_property_changing_listener(self,
        listener: PropertyChangingListenerProtocol):
        pass

    def remove_property_changing_listener(self,
        listener: PropertyChangingListenerProtocol):
        pass

class Product:
    def __init__(self, price: float, rate: float, availability: bool,
                 listeners: list[PropertyChangingListenerProtocol]) -> None:
        self._price = price
        self._rate = rate
        self._availability = availability
        self._listeners = listeners

    def add_property_changed_listener(self,
                                      listener: PropertyChangedListenerProtocol):
        pass

class Followers:
    pass