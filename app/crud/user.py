from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

# CRUD

# TODO: Criar TESTES
# CREATE user
def crud_create_user(db: Session, new_user: UserCreate):
    # Conversão para dict
    user_data = new_user.model_dump() # <-------- faz a conversão para dict, diferente de model_config

    # '**' desempacota
    user = User(**user_data)

    db.add(user)
    db.commit()
    db.refresh(user) # Segundo discussões ele sincroniza o objeto com a versão que está no banco de dados

    return user
# GET user
# GET users
# UPDATE user
# DELETE user