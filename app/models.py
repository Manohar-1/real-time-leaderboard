from sqlalchemy import Column, Integer, String

from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    score = Column(Integer, default=0)

