from database.db import Base, engine
from models.user import User
from models.post import Post

Base.metadata.create_all(bind=engine)