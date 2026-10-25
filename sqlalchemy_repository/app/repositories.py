from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import User

class UserRepository:
    def __init__(self, db:Session):
        self.db = db
    
    def create(self, name:str, email:str) -> User:
        user = User(name=name, email=email)

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def get_by_id(self, user_id:int) -> User | None:
        return self.db.get(User, user_id)
    
    def get_by_email(self, email:str) -> User | None:
        statement = select(User).where(User.email == email)
        return self.db.scalars(statement).first()
    
    def list_all(self) -> list[User]:
        statement = select(User).order_by(User.id)
        return list(self.db.scalars(statement).all())
    
    def update(
        self,
        user_id: int,
        name: str | None = None,
        email: str | None = None,
    ) -> User | None:
        user = self.get_by_id(user_id)

        if user is None:
            return None
        
        if name is not None:
            user.name = name
        
        if email is not None:
            user.email = email

        self.db.commit()
        self.db.refresh(user)

        return user
    
    def delete(
        self,
        user_id: int,
    ) -> bool:
        user = self.get_by_id(user_id)
        if user is None:
            return False
        
        self.db.delete(user)
        self.db.commit()

        return True