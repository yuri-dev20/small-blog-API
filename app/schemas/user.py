from pydantic import BaseModel, ConfigDict
from typing import Optional

# Base Model é usado para a validação tanto de entrada (Se os dados são válidos) quanto para a saída (Como será o retorno) nas API's 
class UserBase(BaseModel):
    name: str
    email: str
    password: str
    admin: bool
    user_active: bool

    """
    Isso permite que o Pydantic leia atributos de objetos e não apenas de dicionários já que Pydantic só aceita dados em formato de dicionário

    Ja que o SQLAlchemy retorna um objeto e a conversão é feita automaticamente
    """
    model_config = ConfigDict(from_attributes = True)

# Ia herdar de 'UserBase' mas iria retornar a password
class UserOut(BaseModel):
    id: int
    name: str
    email: str
    admin: bool
    user_active: bool

    model_config = ConfigDict(from_attributes = True)

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    admin: Optional[bool] = None
    user_active: Optional[bool] = None

    model_config = ConfigDict(from_attributes = True)