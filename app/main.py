from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from .database import Base, engine
from .schema import schema

app = FastAPI()
graphql_app = GraphQLRouter(schema)

Base.metadata.create_all(bind=engine)

app.include_router(graphql_app, prefix="/graphql")
