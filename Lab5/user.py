from dataclasses import dataclass, field
from typing import Optional

@dataclass
class User:
    id: int
    name: str
    login: str
    password: Optional[str] = field(repr=False, default=None)
    email: Optional[str] = None
    address: Optional[str] = None

    def __lt__(self, other: object) -> bool:
        if isinstance(other, User):
            return self.name < other.name
        else:
            return NotImplemented

    def __eq__(self, other: object) -> bool:
        if isinstance(other, User):
            return self.name == other.name
        else:
            return NotImplemented

@dataclass
class UserRegistration:
    id: int
    name: str
    login: str
    password: str
    email: Optional[str] = None
    address: Optional[str] = None

@dataclass
class PasswordRecord:
    id: int
    login: str
    password_hash: str


