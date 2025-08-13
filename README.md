# SMALL BLOG API

Com ajuda da documentação, leituras e vídeos decidi que a melhor introdução ao framework FastAPI seria construindo um projeto
e registrando a jornada até o fim.

O projeto a seguir tem como rotas a criação de usuários e seus respectivos cruds em uma base de dados sqlite tendo em vista o escopo
pequeno do projeto, e com auxilio de bibliotecas de autorização e autenticação garantir aos usuários válidos a possibilidade de fazer
operações em rotas de Post.

## Bibliotecas
- [SQLAlchemy](https://docs.sqlalchemy.org/en/20/)
- [FastAPI](https://fastapi.tiangolo.com/learn/)
- [Pydantic](https://docs.pydantic.dev/latest/)
- [PyJWT](https://pyjwt.readthedocs.io/en/stable/)
- [passlib](https://passlib.readthedocs.io/en/stable/)
- [PyTest](https://docs.pytest.org/en/stable/)
- [dotenv](https://pypi.org/project/python-dotenv/)


## Instalação

Clone o projeto
```bash
    git clone https://github.com/yuri-dev20/small-blog-API
```

Entre no diretorio no projeto
```bash
    cd small-blog-API
```

Crie um ambiente virtual
```bash
    python -m venv ".venv"
```

Inicie ambiente virtual / WINDOWS
```bash
    .\.venv\Scripts\activate
```

Instale as dependências
```bash
    pip install -r requirements.txt
```

Vá para a pasta app
```bash
   cd app
```

No terminal rode
```bash
   fastapi dev main.py
```

## Rota de Users

### Retorna todos os usuários
```http
    GET /users
```

### Retorna um usuário
```http
    GET /users/{user_id}
```

### Cria um usuário
```http
    POST /users
```

### Atualiza um usuário
```http
    PUT /users/{user_id}
```

### Deleta um usuário
```http
    DELETE /users/{user_id}
```

## Rota de Posts

Utilizando o JWT e OAuth2 retorne um token que autorize as rotas bloqueadas, a ideia e que cada usuário seja válido caso ele exista no banco, 
o hash da senha guardada no banco seja igual a senha enviada isso é verificado pela biblioteca passlib e seu modulo CryptContext

### Retorna todos os posts do usuário 
```http
    GET /users/me/posts
```

### Retorna um post do usuário 
```http
    GET /users/me/posts/{post_id}
```

### Cria um post
```http
    POST /users/me/posts
```

### Atualiza o post do usuário
```http
    PUT /users/me/posts/{post_id}
```

### Deleta um post do usuário
```http
    DELETE /users/me/posts/{post_id}
```

## Rodando testes

Na pasta de tests rode o comando
```bash
    pytest -q -v
```