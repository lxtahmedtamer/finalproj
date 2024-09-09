from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
# Create the database tables
models.Base.metadata.create_all(bind=engine)



app = FastAPI()

# Allow CORS for frontend's domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods like POST, PUT, DELETE, etc.
    allow_headers=["*"],  # Allow all headers
)
# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/todos", response_model=list[schemas.ToDo], status_code=status.HTTP_200_OK)
def get_todos(db: Session = Depends(get_db)):
    todos = crud.get_todos(db)
    if not todos:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No ToDos found.")
    return todos


@app.post("/todos", response_model=schemas.ToDo, status_code=status.HTTP_201_CREATED)
def add_todo(todo: schemas.ToDoCreate, db: Session = Depends(get_db)):
    new_todo = crud.create_todo_item(db, todo)
    return new_todo


@app.put("/todos/{todo_id}", response_model=schemas.ToDo, status_code=status.HTTP_200_OK)
def toggle_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = crud.toggle_todo_item(db, todo_id)
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ToDo item not found.")
    return todo


@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo_deleted = crud.delete_todo_item(db, todo_id)
    if todo_deleted is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ToDo item not found.")
    return {"message": "ToDo item successfully deleted"}
