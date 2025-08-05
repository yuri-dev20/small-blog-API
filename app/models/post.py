from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base
from .user import User

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    text = Column(String)

    owner_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
    # Relacionamento e ainda precisa bater com o nome no 'user.py'
    user = relationship('User', back_populates='posts')