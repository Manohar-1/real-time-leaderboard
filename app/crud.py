from sqlalchemy.orm import Session
from app import models, schemas
from app.security import hash_password,verify_password
from app.models import User
from app.schemas import UserLogin
from app.redis_client import redis_client


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username, email=user.email, password=hash_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# def get_leaderboard(db: Session,limit:int,offset:int):
#     return db.query(models.User).order_by(models.User.score.desc()).offset(offset).limit(limit).all()

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username==username).first()


# def get_user_score(db:Session, username:str):
#     user = get_user_by_username(db,username)
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user.score

def get_user_game_score(db:Session, user_id:int, game:str):
    return db.query(models.Score).filter(models.Score.user_id==user_id, models.Score.game==game).first()

# def get_user_rank(db:Session, score:int):
#     higher_score_count = db.query(User).filter(User.score > score).count()
#     rank = higher_score_count + 1
#     return rank

def authenticate_user(db: Session, user: UserLogin):
    db_user = get_user_by_username(db,user.username)
    
    if db_user is None:
        return False

    if not verify_password(user.password, db_user.password):
        return None
    
    return db_user



def submit_score(db:Session, user_id:int, game:str, score:int):
    existing_score = get_user_game_score(db, user_id, game)
    
    if existing_score:
        if score > existing_score.score:
            existing_score.score = score
            db.commit()
            db.refresh(existing_score)
    else:
        new_score = models.Score(user_id=user_id, game=game, score=score)
        db.add(new_score)
        db.commit()
        db.refresh(new_score)

    aggregate_score = get_user_aggregate_score(db, user_id)
    redis_client.zadd('global_leaderboard',{str(user_id):aggregate_score})
    return get_user_game_score(db,user_id, game)


    
def delete_user(db: Session, username:str):
    user = get_user_by_username(db,username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": f"account with username {username} deleted successfully"}

def update_user(user_data: schemas.UserUpdate, username:str, db: Session):
    user = get_user_by_username(db,username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user_data.email is not None:
        user.email = user_data.email
    
    if user_data.password is not None:
        user.password = hash_password(user_data.password)
    
    db.commit()
    db.refresh(user)
    return user

def get_user_aggregate_score(db: Session, user_id: int):
    total_score = db.query(models.Score).filter(models.Score.user_id == user_id).all()
    return sum(score.score for score in total_score)
