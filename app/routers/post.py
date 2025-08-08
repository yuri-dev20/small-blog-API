from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Annotated
from app.database.db import get_db

from app.schemas.post import PostCreate, PostOut, PostUpdate

from app.crud.post import (
    crud_create_post,
    crud_read_all_posts,
    crud_read_post,
    crud_update_post
)

router = APIRouter(
    # o id será extraido desta url
    prefix='/users/{user_id}/posts',
    tags=['Posts']
)

# CREATE post
@router.post('/', response_model=PostOut)
def create_post(db: Annotated[Session, Depends(get_db)], user_id: int, new_post: PostCreate):
    post = crud_create_post(db, user_id, new_post)

    if not post:
        raise HTTPException(status_code=404, detail=f"Usuário de id {user_id} não existe")
    
    return post
    
# GET posts
@router.get('/', response_model=List[PostOut])
def get_all_posts(db: Annotated[Session, Depends(get_db)], user_id: int, limit: int = None):
    posts = crud_read_all_posts(db, user_id)
    
    if not posts:
        raise HTTPException(status_code=404, detail=f"Posts não encontrados ou não pertencem ao usuário")
    
    if limit:   
        return posts[:limit]
    
    return posts

# GET post
@router.get('/{post_id}', response_model=PostOut)
def get_post(db: Annotated[Session, Depends(get_db)], user_id: int, post_id: int):
    post = crud_read_post(db, user_id, post_id) 
    
    if not post:
        raise HTTPException(status_code=404, detail=f"Post não encontrado ou não pertence ao usuário")
    
    return post

# UPDATE post
"""
Isso é provisorio pois a ideia e usar JWT no projeto e bcrypt no projeto ainda
"""
@router.put('/{post_id}', response_model=PostOut)
def update_post(db: Annotated[Session, Depends(get_db)], user_id: int, post_id: int, update_post_data: PostUpdate):
    post = crud_update_post(db, user_id, post_id, update_post_data)

    if not post:
        raise HTTPException(status_code=404, detail=f"Post não encontrado ou não pertence ao usuário")
    
    return post