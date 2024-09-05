from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import engine, get_db

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/todos", response_model=list[schemas.ToDo])
def get_todos(db: Session = Depends(get_db)):
    return crud.get_todos(db)

@app.post("/todos", response_model=schemas.ToDo)
def add_todo(todo: schemas.ToDoCreate, db: Session = Depends(get_db)):
    return crud.create_todo_item(db, todo)

@app.put("/todos/{todo_id}", response_model=schemas.ToDo)
def toggle_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = crud.toggle_todo_item(db, todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="ToDo item not found")
    return todo

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    crud.delete_todo_item(db, todo_id)
    return {"message": "ToDo item deleted"}
