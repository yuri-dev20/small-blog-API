from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import relationship
from database.db import Base

# Representa uma tabela do DB ao herdar do Base
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    admin = Column(Boolean)
    user_active = Column(Boolean)

    posts = relationship('Post', back_populates='user', cascade='all, delete')