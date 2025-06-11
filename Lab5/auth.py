from abc import ABC, abstractmethod
from typing import Optional
import hashlib
from user import User,  UserRegistration
from repository import IUserRepository, PasswordRepository, PasswordRecord
from session import SessionStorage, Session

class IAuthService(ABC):
    @abstractmethod
    def sign_in(self, login: str, password: str) -> Optional[User]:
        ...

    @abstractmethod
    def sign_out(self) -> None:
        ...

    @abstractmethod
    def is_authorized(self) -> bool:
        ...

    @abstractmethod
    def current_user(self) -> Optional[User]:
        ...


class AuthService(IAuthService):
    def __init__(
        self,
        user_repo: IUserRepository,
        password_repo: PasswordRepository,
        session_storage: "SessionStorage"
    ):
        self.user_repo = user_repo
        self.password_repo = password_repo
        self.session_storage = session_storage
        self._current_user: Optional[User] = None

        try:
            session = self.session_storage.load()
            if session:
                user = self.user_repo.get_by_login(session.login)
                if user:
                    self._current_user = user
        except Exception as e:
            print(f"Ошибка при загрузке сессии: {e}")

    def _hash(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def sign_in(self, login: str, password: str) -> Optional[User]:
        try:
            user = self.user_repo.get_by_login(login)
            if not user:
                print("Пользователь не найден.")
                return None

            pwd_record = self.password_repo.get_by_login(login)
            if not pwd_record:
                print("Пароль для пользователя не найден.")
                return None

            if pwd_record.password_hash != self._hash(password):
                print("Неверный пароль.")
                return None

            self._current_user = user
            new_session = Session(login=login)
            self.session_storage.save(new_session)
            return user

        except Exception as e:
            print(f"Ошибка при входе: {e}")
            return None

    def sign_out(self) -> None:
        try:
            self._current_user = None
            self.session_storage.clear()
        except Exception as e:
            print(f"Ошибка при выходе из системы: {e}")

    def is_authorized(self) -> bool:
        return self._current_user is not None

    def current_user(self) -> Optional[User]:
        return self._current_user

    def register_user(self, reg: UserRegistration) -> Optional[User]:
        if self.user_repo.get_by_login(reg.login):
            print(f"Ошибка регистрации: пользователь '{reg.login}' уже существует.")
            return None
        new_user = User(
            id=reg.id,
            name=reg.name,
            login=reg.login,
            email=reg.email,
            address=reg.address
        )
        self.user_repo.add(new_user)
        pwd_record = PasswordRecord(
            id=new_user.id,
            login=new_user.login,
            password_hash=self._hash(reg.password)
        )
        self.password_repo.add(pwd_record)
        self._current_user = new_user
        self.session_storage.save(Session(login=new_user.login))
        return new_user

