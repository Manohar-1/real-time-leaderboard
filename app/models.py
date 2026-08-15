from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
     
    #back_populates referes to the "user" attribute in the Score model
    scores = relationship("Score", back_populates="user")

class Score(Base):
    __tablename__ = "scores"

    __table_args__ = (UniqueConstraint("user_id", "game", name="unique_user_game"),)

    id= Column(Integer, primary_key=True)
    user_id = Column(Integer,ForeignKey('users.id'),nullable=False)
    game = Column(String, nullable=False)
    score = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    #back_populates refers to the "scores" attribute in the User model
    user = relationship("User", back_populates="scores")

