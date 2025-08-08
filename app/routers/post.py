from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Annotated
from app.database.db import get_db

from app.schemas.post import PostCreate, PostOut, PostUpdate

from app.crud.post import (
    crud_create_post,
)

router = APIRouter(
    # o id será extraido desta url
    prefix='/users/{user_id}/posts',
    tags=['Posts']
)

@router.post('/', response_model=PostOut)
def create_post(db: Annotated[Session, Depends(get_db)], user_id: int, new_post: PostCreate):
    post = crud_create_post(db, user_id, new_post)

    if not post:
        raise HTTPException(status_code=404, detail=f"Usuário de id {user_id} não existe")
    
    return post
    