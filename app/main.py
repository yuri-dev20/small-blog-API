from fastapi import FastAPI
from app.database.db import Base, engine

from app.routers import user
from app.routers import post

# Enquanto desenvolvo testes isso fica fora pois não quero que o outra DB seja criada 
# Base.metadata.create_all(bind=engine)

app = FastAPI(title="Small Blog")

app.include_router(user.router)
app.include_router(post.router)