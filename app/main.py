from fastapi import FastAPI,Depends
from app.database import Base, engine
from app import models,crud
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.schemas import UserCreate

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def hello_world():
    return "Hello, World!"


@app.post("/users")
def create_user(user:UserCreate,db: Session = Depends(get_db)):
    return crud.create_user(db,user)