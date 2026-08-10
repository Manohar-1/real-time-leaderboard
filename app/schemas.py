from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    password : str

class UserLogin(BaseModel):
    username: str
    password: str

class SubmitScore(BaseModel):
    score:int

class LeaderBoardUser(BaseModel):
    username: str
    score: int