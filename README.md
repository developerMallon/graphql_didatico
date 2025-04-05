Vamos montar uma aplicação didática com **FastAPI**, **SQLAlchemy** e **GraphQL (Strawberry)** com as rotas básicas para:

- Criar um usuário
- Listar usuários
- Atualizar usuário
- Excluir usuário

O modelo `User` terá os campos: `id`, `nome`, `email` e `senha`.

---

### 📁 Estrutura do Projeto (mínima)
```
app/
├── main.py
├── models.py
├── schema.py      # GraphQL
├── database.py
└── crud.py
```

---

### `requirements.txt`
```txt
fastapi
uvicorn
sqlalchemy
strawberry-graphql
pydantic
databases
aiofiles
```

---

### `database.py`
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()
```

---

### `models.py`
```python
from sqlalchemy import Column, Integer, String
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    senha = Column(String, nullable=False)
```

---

### `crud.py`
```python
from sqlalchemy.orm import Session
from .models import User

def create_user(db: Session, nome: str, email: str, senha: str):
    user = User(nome=nome, email=email, senha=senha)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_users(db: Session):
    return db.query(User).all()

def update_user(db: Session, user_id: int, nome: str, email: str, senha: str):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.nome = nome
        user.email = email
        user.senha = senha
        db.commit()
        db.refresh(user)
    return user

def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user
```

---

### `schema.py` (GraphQL com Strawberry)
```python
import strawberry
from typing import List
from .models import User
from .database import SessionLocal
from . import crud

@strawberry.type
class UserType:
    id: int
    nome: str
    email: str
    senha: str

@strawberry.type
class Query:
    @strawberry.field
    def users(self) -> List[UserType]:
        db = SessionLocal()
        return crud.get_users(db)

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_user(self, nome: str, email: str, senha: str) -> UserType:
        db = SessionLocal()
        return crud.create_user(db, nome, email, senha)

    @strawberry.mutation
    def update_user(self, id: int, nome: str, email: str, senha: str) -> UserType:
        db = SessionLocal()
        return crud.update_user(db, id, nome, email, senha)

    @strawberry.mutation
    def delete_user(self, id: int) -> UserType:
        db = SessionLocal()
        return crud.delete_user(db, id)

schema = strawberry.Schema(query=Query, mutation=Mutation)
```

---

### `main.py`
```python
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from .database import Base, engine
from .schema import schema

app = FastAPI()
graphql_app = GraphQLRouter(schema)

Base.metadata.create_all(bind=engine)

app.include_router(graphql_app, prefix="/graphql")
```

---

### 🎯🕹️ Preparando o ambiente virtual e iniciando o projeto
Criar ambiente virtual
```bash
python -m venv venv
```
Iniciar o ambiente virtual
```bash
.\venv\Scripts\activate
```
Instalar as dependências listadas no arquivo requirements.txt
```bash
pip install -r .\requirements.txt
```
Iniciar o projeto
```bash
uvicorn app.main:app --reload 
```

---

### 🧪 Exemplo de uso via Playground `/graphql`
```graphql
# Criar usuário
mutation {
  createUser(nome: "João", email: "joao@email.com", senha: "123456") {
    id
    nome
    email
  }
}

# Listar
query {
  users {
    id
    nome
    email
  }
}

# Atualizar
mutation {
  updateUser(id: 1, nome: "João Silva", email: "joao@email.com", senha: "novasenha") {
    id
    nome
    email
  }
}

# Excluir
mutation {
  deleteUser(id: 1) {
    id
    nome
  }
}
```

---
