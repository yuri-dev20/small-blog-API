from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Annotated
from app.database.db import get_db

from app.models.user import User
from app.schemas.user import UserOut, UserCreate, UserUpdate

from app.crud.user import (
    crud_create_user,
    crud_read_users,
    crud_read_user
)

router = APIRouter(
    prefix='/users', 
    tags=['Users'])

# CREATE user
@router.post('/', response_model=UserOut)
def create_user(db: Annotated[Session, Depends(get_db)], new_user: UserCreate):
    # Annotated permite introduzir/adcionar metadados
    # Traduzindo para português ficaria tipo: 'Crie um parâmetro chamado db que é do tipo Session, e para obter seu valor, execute a função get_db()'

    user_verify = db.query(User).filter(User.email == new_user.email).first()
    if user_verify:
        raise HTTPException(status_code=409, detail='Email já cadastrado')

    response = crud_create_user(db, new_user)
    return response

# GET/READ users
@router.get('/', response_model=List[UserOut])
def get_users(db: Annotated[Session, Depends(get_db)], limit: int = None):
    if limit:
        users = crud_read_users(db)
        return users[:limit]
    
    else:
        return crud_read_users(db)

@router.get('/{user_id}', response_model=UserOut)
def get_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    return crud_read_user(db, user_id)