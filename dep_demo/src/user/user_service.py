from typeguard import typechecked
from user.user import User

@typechecked
class UserService:

    # MockDB
    _users = []

    def all(self) -> list:
        return [dict(user) for user in self._users]

    def find_by_email(self, email: str) -> dict | None:
        return next((dict(user) for user in self._users if user.email == email), None)
    
    def save(self, user: User):
        exists = self.find_by_email(user.email)
        if exists:
            raise Exception(f"user {user.email} alredy exists")
        
        return self._users.append(user)

    def delete(self, user: User) -> None:
        exists = self.find_by_email(user.email)
        if not exists:
            raise Exception(f"user {user.email} not exists")
        
        self._users.remove(user)

    def update(self, user: User) -> None:
        exists = self.find_by_email(user.email)
        if not exists:
            raise Exception(f"user {user.email} not exists")
        
        self._users[self._users.index(User(**exists))] = user

