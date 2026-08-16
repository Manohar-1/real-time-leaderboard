from pydantic import BaseModel
from enum import Enum

class UserCreate(BaseModel):
    username: str
    email: str
    password : str

class UserLogin(BaseModel):
    username: str
    password: str

class UserProfile(BaseModel):
    username: str
    email: str
    score: int
    rank: int



class ScoreCreate(BaseModel):
    game : GameType
    score:int

class GameType(str, Enum):
    CHESS = "chess"
    FOOTBALL = "football"

# class LeaderBoardUser(BaseModel):
#     username: str
#     score: int

class UserRank(BaseModel):
    username:str
    score:int
    rank:int

class UserUpdate(BaseModel):
    email: str | None = None
    password: str | None = None