from fastapi import FastAPI
from database.db import Base, engine

from routers import user
from routers import post

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Small Blog")

app.include_router(user.router)
app.include_router(post.router)