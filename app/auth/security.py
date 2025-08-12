from passlib.context import CryptContext
from dotenv import load_dotenv
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from typing import Annotated
from sqlalchemy.orm import Session

from app.schemas.token import TokenData
from app.auth.service import get_user
from app.database.db import get_db

import jwt
import os
"""
    CryptContext armazena configurações dos algoritmos usados para o hash

    schemas = algoritmo usado no hash
""" 
load_dotenv()

# assina (criptografa) os tokens JWT para garantir que só seu servidor consiga validar eles.
SECRET_KEY = os.getenv('SECRET_KEY')
# Aparententemente o segundo diz que caso o primeiro falhe use ele
ALGORITHM = os.getenv('ALGORITHM', 'HS256')
ACCESS_TOKEN_EXPIRE = int(os.getenv('ACCESS_TOKEN_EXPIRE'))

"""
    OAuth2PasswordBearer é uma classe do fastapi que cria uma dependencia para pegar o token que é enviado pelo cliente/user
    Ele espera exatamente um formato Authorization: Bearer na requisição
"""
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def verify_password(plain_password: str, hashed_password: str):     # Verifique a senha enviada pelo user com a senha armazenada
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str):
    # Gere um hash com a senha enviada
    return pwd_context.hash(password)

"""
    data = dict de informações com o que será codificado dentro do token
    expire_delta = tempo opcional que se não for definido usará o padrão definido na função
"""
def create_access_token(data: dict, expire_delta: timedelta | None = None):
    # A cópia será o payload do token
    to_encode = data.copy()
    
    if expire_delta:
        expire = datetime.now(timezone.utc) + expire_delta

    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE)

    # Uma informação padrão dentro do token é o 'exp' que define o tempo de vida do token e aki estamos a adcionando
    to_encode.update({
        'exp': expire
    })

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt # O resultado é uma string codificada que representa o token seguro

def get_current_user(db: Annotated[Session, Depends(get_db)], token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=401,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get('sub')

        if email is None:
            raise credentials_exception
        
        token_data = TokenData(email=email)

    except InvalidTokenError:
        raise credentials_exception
    
    user = get_user(db, token_data.email)
    
    if user is None:
        raise credentials_exception
    
    return user