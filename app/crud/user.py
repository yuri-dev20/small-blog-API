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
# DELETE user