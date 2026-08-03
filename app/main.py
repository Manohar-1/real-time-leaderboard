from fastapi import FastAPI,Depends
from app.database import Base, engine
from app import models,crud,schemas
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.schemas import UserCreate
from app.security import verify_password



app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def hello_world():
    return "Hello, World!"


@app.post("/users")
def create_user(user:UserCreate,db: Session = Depends(get_db)):
    return crud.create_user(db,user)

@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, user.username)

    if not db_user:
        return {"error": "Invalid username or password"}
    
    if not verify_password(user.password, db_user.password):
        return {"error": "Invalid username or password"}

    return {"message": "Login successful"}
    