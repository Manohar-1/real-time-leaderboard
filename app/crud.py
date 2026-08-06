from sqlalchemy.orm import Session
from app import models, schemas
from app.security import hash_password,verify_password
from app.models import User
from app.schemas import UserLogin


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username, email=user.email, password=hash_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username==username).first()

def authenticate_user(db: Session, user: UserLogin):
    db_user = get_user_by_username(db,user.username)
    
    if db_user is None:
        return False

    if not verify_password(user.password, db_user.password):
        return None
    
    return db_user

def update_user_score(db: Session, username:str, score:int):
    user = get_user_by_username(db,username)
    user.score = score
    db.commit()
    db.refresh(user)
    return user