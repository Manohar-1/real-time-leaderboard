from fastapi import FastAPI,Depends, HTTPException, Query
from app.database import Base, engine
from app import models,crud,schemas
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.schemas import UserCreate
from app.security import verify_password
from app.auth import create_access_token
from app.auth import get_current_user

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def hello_world(db: Session = Depends(get_db)):
    # print(crud.get_user_score(db,username="rahul"))
    return "Hello, World!"


@app.post("/users")
def create_user(user:UserCreate,db: Session = Depends(get_db)):
    return crud.create_user(db,user)

@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.authenticate_user(db, user)
    if db_user is None or db_user is False:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    access_token = create_access_token(data={"sub":db_user.username})    
    return {"access_token": access_token,"token_type": "bearer"}
    
# @app.get("/me")
# def read_current_user(current_user:str = Depends(get_current_user)):
#     return {"username": current_user}

@app.post("/submit_score")
def submit_score(score_update: schemas.SubmitScore, current_user:str = Depends(get_current_user), db: Session = Depends(get_db)):
    updated_user = crud.submit_score(db, current_user, score_update.score)
    return {"username": updated_user.username, "score": updated_user.score}

@app.get("/leaderboard",response_model=list[schemas.LeaderBoardUser])
def get_leaderboard(limit:int=Query(10,ge=1,le=100),offset:int=Query(0,ge=0),db: Session = Depends(get_db)):
    return crud.get_leaderboard(db,limit,offset)

@app.get("/me/rank",response_model = schemas.UserRank)
def get_my_rank(db:Session = Depends(get_db), username:str = Depends(get_current_user)):
    user_score = crud.get_user_score(db,username)
    rank = crud.get_user_rank(db,user_score)
    return {"username": username, "score": user_score, "rank": rank}