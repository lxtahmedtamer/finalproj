from sqlalchemy.orm import Session
import models
from models import ToDoItem
import schemas
from schemas import ToDoBase, ToDoCreate,ToDo
###
#def get_todos(db: Session):
 #   return db.query(models.ToDoItem).all()

#def create_todo_item(db: Session, todo: schemas.ToDoCreate):
   # db_todo = models.ToDoItem(text=todo.text,completed=todo.completed)
  #  db.add(db_todo)
 #   db.commit()
#    db.refresh(db_todo)
#    return db_todo
#


def get_todos_by_user(db: Session, user_id: int):
    return db.query(models.ToDo).filter(models.ToDo.owner_id == user_id).all()

def create_todo_item(db: Session, todo: schemas.ToDoCreate, user_id: int):
    db_todo = models.ToDo(**todo.dict(), owner_id=user_id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def toggle_todo_item(db: Session, todo_id: int):
    todo = db.query(models.ToDoItem).filter(models.ToDoItem.id == todo_id).first()
    if todo:
        todo.completed = not todo.completed
        db.commit()
    return todo

def delete_todo_item(db: Session, todo_id: int):
    db.query(models.ToDoItem).filter(models.ToDoItem.id == todo_id).delete()
    db.commit()
