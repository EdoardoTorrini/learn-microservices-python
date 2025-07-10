from sqlalchemy.orm import Session

from user.model import User
from user.dto import UserDTO

from datetime import datetime


class UserService:

    @staticmethod
    def get_all(db: Session):
        return db.query(User).all()
    
    @staticmethod
    def get_user_by_id(db: Session, uuid: str):
        return db.query(User).filter(User.user_uuid == uuid).first()
    
    @staticmethod
    def create(db: Session, user: UserDTO) -> User:
        new_user = User(
            user_uuid=user.uuid,
            nickname=user.nickname,
            birthday=datetime.strptime(user.birthday,'%d-%m-%Y')
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user