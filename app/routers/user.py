from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Annotated
from app.database.db import get_db

from app.models.user import User
from app.schemas.user import UserOut, UserCreate, UserUpdate

from app.crud.user import (
    crud_create_user,
    crud_read_users,
    crud_read_user,
    crud_update_user,
    crud_delete_user
)

router = APIRouter(
    prefix='/users', 
    tags=['Users'])

# CREATE user
@router.post('/', response_model=UserOut)
def create_user(db: Annotated[Session, Depends(get_db)], new_user: UserCreate):
    # Annotated permite introduzir/adcionar metadados
    # Traduzindo para português ficaria tipo: 'Crie um parâmetro chamado db que é do tipo Session, e para obter seu valor, execute a função get_db()'
    response = crud_create_user(db, new_user)
    
    if not response:
        raise HTTPException(status_code=409, detail='Email já cadastrado')
    
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

# UPDATE user
@router.put('/{user_id}', response_model=UserOut)
def update_user(db: Annotated[Session, Depends(get_db)], update_user_data: UserUpdate, user_id: int):
    user = crud_update_user(db, update_user_data, user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail=f"Usuário de id: {user_id} não encontrado")
    
    else:
        return user
    
# DELETE user
@router.delete('/{user_id}', response_model=UserOut)
def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = crud_delete_user(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail=f"Usuário de id: {user_id} não encontrado")
    
    else:
        return user