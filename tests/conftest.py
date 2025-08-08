"""
'conftest.py' é um arquivo utilizado para definição de fixtures, recursos e configurações que 
são compartilhados entre os arquivos de teste
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app, Base
from app.database.db import get_db
from app.models.user import User
from app.models.post import Post

# Banco fake SQLite
DB_URL = 'sqlite:///./test_blog.db'
engine = create_engine(
    DB_URL,
    connect_args={'check_same_thread': False}
)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Fixtures são setups ou um modo de preparar dados, configurações e recursos, funciona como uma 'injeção de independencia'
# 'scope' é bem simples segundo leituras define o escopo de vida, quando será criado ou destruido
# scope='function' ---> função roda antes de cada teste, é criado antes de cada teste e destruído dps
@pytest.fixture(scope='function')
def db_test():
    # Como mencionado a fixture cria e destroi o banco de dados para cada teste
    Base.metadata.create_all(bind=engine)
    session_test = TestSessionLocal()

    try:
        yield session_test

    finally:
        session_test.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope='function')
def client_test(db_test):
    """
    Fixture que cria o cliente que será utilizado nos testes

    'db_test' = fixture criada acima
    'yield db_test' = retorna o banco de teste ao invés do real usado no 'app'
    """
    def override_get_db():
        try:
            yield db_test
        
        finally:
            db_test.close()

    # Substitui um por outro, auto explicativo
    # todos os bancos que usarem Depends[get_db] usaram o de test
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client # entrega ou joga o cliente para os testes, entenda isso como uma navegador falso que irá usar a API

    app.dependency_overrides.clear() # Limpa os overrides


@pytest.fixture
def sample_user(db_test):
    # fixture simples que cria um usuario como exemplo
    user = User(
        name="Jhon Doe",
        email="jhondoe@gmail.com",
        password="coxinha123",
        admin=0,
        user_active=1
    )

    db_test.add(user)
    db_test.commit()
    db_test.refresh(user)
    
    return user

@pytest.fixture
def sample_post(db_test, sample_user):
    post = Post(
        title="Testing post",
        text="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        owner_id=sample_user.id
    )

    db_test.add(post)
    db_test.commit()
    db_test.refresh(post)
    
    return post