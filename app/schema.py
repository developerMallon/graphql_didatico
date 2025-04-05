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
