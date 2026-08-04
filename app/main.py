from fastapi import FastAPI,Depends, HTTPException
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
    db_user = crud.authenticate_user(db, user)
    
    if db_user is None or db_user is False:
        raise HTTPException(status_code=401, detail="Invalid username or password")
        
    return {"message": "Login successful"}
    