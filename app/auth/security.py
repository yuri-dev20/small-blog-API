from passlib.context import CryptContext

"""
    CryptContext armazena configurações dos algoritmos usados para o hash

    schemas = algoritmo usado no hash
""" 

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def verify_password(plain_password: str, hashed_password: str):     # Verifique a senha enviada pelo user com a senha armazenada
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str):
    # Gere um hash com a senha enviada
    return pwd_context.hash(password)
