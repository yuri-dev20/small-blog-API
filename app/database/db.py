from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine, event

"""
Engine que é usado 'conversar' com o BD
connect_args={'check_same_thread': False - permite que a mesma conexão com o banco de dados seja usada por vária threads
"""
engine = create_engine('sqlite:///mydb.db', connect_args={'check_same_thread': False}, echo=True)

# uma sessão seria um 'operador' que faz as operações com o banco e aqui ele é definido
SessionLocal = sessionmaker(bind=engine, autocommit=False)

# Base serve como uma fabrica de metaclasses, quando uma classe herda dele ela se torna uma entidadde ORM e representa uma tabela do DB
# e é com Base que criamos as tabelas
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db

    finally:
        db.close()

# decorador que 'escuta' quando o DB for conectado
@event.listens_for(engine, "connect")
# dbapi_connection conexão com o banco
def set_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    # executa PRAGMA foreign_keys=ON que ativa a constraints como ON DELETE CASCADE
    cursor.execute('PRAGMA foreign_keys=ON;')
    cursor.close()