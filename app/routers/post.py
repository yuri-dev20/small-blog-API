from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Annotated
from app.database.db import get_db

from app.schemas.post import PostCreate, PostOut, PostUpdate
from app.models.user import User
from app.auth.security import get_current_user

from app.crud.post import (
    crud_create_post,
    crud_read_all_posts,
    crud_read_post,
    crud_update_post,
    crud_delete_post
)

router = APIRouter(
    # o id será extraido desta url
    prefix='/users/me/posts',
    tags=['Posts'],
    dependencies=[Depends(get_current_user)]
)

# CREATE post
@router.post('/', response_model=PostOut)
def create_post(db: Annotated[Session, Depends(get_db)], current_user: Annotated[User, Depends(get_current_user)], new_post: PostCreate):
    post = crud_create_post(db, current_user.id, new_post)

    if not post:
        raise HTTPException(status_code=400, detail=f"Não foi possível criar o post")
    
    return post
    
# GET posts
@router.get('/', response_model=List[PostOut])
def get_all_posts(db: Annotated[Session, Depends(get_db)], current_user: Annotated[User, Depends(get_current_user)], limit: int = None):
    posts = crud_read_all_posts(db, current_user.id)
    
    if limit:   
        return posts[:limit]
    
    # Aqui retorna vazia se não houver nada
    return posts

# GET post
@router.get('/{post_id}', response_model=PostOut)
def get_post(db: Annotated[Session, Depends(get_db)], current_user: Annotated[User, Depends(get_current_user)], post_id: int):
    post = crud_read_post(db, current_user.id, post_id) 
    
    if not post:
        raise HTTPException(status_code=404, detail=f"Post não encontrado ou não pertence ao usuário")
    
    return post

# UPDATE post
@router.put('/{post_id}', response_model=PostOut)
def update_post(
    db: Annotated[Session, Depends(get_db)], 
    current_user: Annotated[User, Depends(get_current_user)], 
    post_id: int, 
    update_post_data: PostUpdate):

    post = crud_update_post(db, current_user.id, post_id, update_post_data)

    if not post:
        raise HTTPException(status_code=404, detail=f"Post não encontrado ou não pertence ao usuário")
    
    return post

# DELETE post
@router.delete('/{post_id}', response_model=PostOut)
def delete_post(db: Annotated[Session, Depends(get_db)], current_user: Annotated[User, Depends(get_current_user)], post_id: int):
    post = crud_delete_post(db, current_user.id, post_id)

    if not post:
        raise HTTPException(status_code=404, detail=f"Post não encontrado ou não pertence ao usuário")
    
    return post