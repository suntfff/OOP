from auth import AuthService
from session import SessionStorage, JsonSessionSerializer
from user import User
from repository import UserRepository, PasswordRepository
from serializer import DataclassJsonSerializer, IDataclassSerializer
from user import UserRegistration, PasswordRecord


def main():
    users_file = 'users.json'
    passwords_file = 'passwords.json'
    session_file = 'session.json'
    user_serializer: IDataclassSerializer[User] = DataclassJsonSerializer(User)
    password_serializer: IDataclassSerializer = DataclassJsonSerializer(PasswordRecord)
    session_serializer = JsonSessionSerializer()
    user_repo = UserRepository(user_serializer, users_file)
    password_repo = PasswordRepository(password_serializer, passwords_file)
    session_storage = SessionStorage(session_file, session_serializer)
    auth_service = AuthService(user_repo, password_repo, session_storage)
    print("Текущий пользователь при запуске")
    if auth_service.is_authorized():
        print(f"Авторизован: {auth_service.current_user().login}")
    else:
        print("Пользователь не авторизован")
    print("\nРегистрация нового пользователя")
    reg1 = UserRegistration(
        id=1,
        name="Пользователь 1",
        login="user1",
        password="qwerty123",
        email="user1@example.com"
    )
    if auth_service.register_user(reg1):
        print(f"Пользователь '{reg1.login}' зарегистрирован и авторизован")
    print("\nРедактирование пользователя")
    user = user_repo.get_by_login("ivan")
    if user:
        user.email = "user_1@example.com"
        user_repo.update(user)
        print(f"Пользователь '{user.login}' обновлен: email={user.email}, address={user.address}")
    print("\nВыход из системы")
    auth_service.sign_out()
    print("Пользователь вышел из системы")
    print("\nАвторизация пользователя")
    user = auth_service.sign_in("user1", "qwerty123")
    if user:
        print(f"Пользователь '{user.login}' успешно авторизован")
    print("\nРегистрация второго пользователя")
    reg2 = UserRegistration(
        id=2,
        name="Пользователь 2",
        login="user2",
        password="qwerty456",
        email="user2@example.com"
    )
    if auth_service.register_user(reg2):
        print(f"Пользователь '{reg2.login}' зарегистрирован и авторизован")

if __name__ == "__main__":
    main()

