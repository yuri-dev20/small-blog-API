from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

# CRUD

# TODO: Criar TESTES
# CREATE user
def crud_create_user(db: Session, new_user: UserCreate):
    user_verify = db.query(User).filter(User.email == new_user.email).first()
    if user_verify:
        return None
    
    # Conversão para dict
    user_data = new_user.model_dump() # <-------- faz a conversão para dict, diferente de model_config

    # '**' desempacota
    user = User(**user_data)

    db.add(user)
    db.commit()
    db.refresh(user) # Segundo discussões ele sincroniza o objeto com a versão que está no banco de dados

    return user

# GET users
def crud_read_users(db: Session):
    # db.execute = executa uma query
    # select(User) = similar a query SQL
    # scalars() = converte o Result em objetos da sua classe ORM ja que sem isso seriam retornados tuplas
    # all() - vira uma lista
    # alternativa ao all()  mas muito legal é o one_or_none()
    return db.execute(select(User)).scalars().all()

# GET users
def crud_read_user(db: Session, id: int):
    # Bagulho verboso do diacho, aparentemente where é prefirido ao invés de filter
    return db.execute(select(User).where(User.id == id)).scalars().one_or_none()

# UPDATE user
def crud_update_user(db: Session, update_user_data: UserUpdate, user_id: int):
    user = db.execute(select(User).where(User.id == user_id)).scalars().one_or_none()

    if user:

        if update_user_data.name is not None:
            user.name = update_user_data.name
        
        if update_user_data.email is not None:
            user.email = update_user_data.email
        
        if update_user_data.password is not None:
            user.password = update_user_data.password

        if update_user_data.admin is not None:
            user.admin = update_user_data.admin

        if update_user_data.user_active is not None:
            user.user_active = update_user_data.user_active


        db.commit()
        db.refresh(user)
        return user
    
    else:
        return None

# DELETE user