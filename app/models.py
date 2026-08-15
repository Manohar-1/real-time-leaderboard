from sqlalchemy import Column, Integer, String

from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    score = Column(Integer,default=0)

class Score(Base):
    __tablename__ = "scores"

    id= Column(Integer, primary_key=True)
    user_id = Column(Integer,ForeignKey('users.id'),nullable=False)
    game = Column(String, nullable=False)
    score = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

