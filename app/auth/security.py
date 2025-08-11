from passlib.context import CryptContext
from dotenv import load_dotenv

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

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def verify_password(plain_password: str, hashed_password: str):     # Verifique a senha enviada pelo user com a senha armazenada
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str):
    # Gere um hash com a senha enviada
    return pwd_context.hash(password)
