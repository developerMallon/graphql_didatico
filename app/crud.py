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
