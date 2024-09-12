from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
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

# OAuth2 scheme for token-based authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to get the current authenticated user (example with token decoding)
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # Decode the token to get the user information (you should implement this logic)
    user = crud.get_user_from_token(db, token)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

# GET todos for the authenticated user
@app.get("/todos", response_model=list[schemas.ToDo], status_code=status.HTTP_200_OK)
def get_todos(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    todos = crud.get_todos_by_user(db, user_id=current_user.id)
    if not todos:
        return []  # Return an empty list if no todos found
    return todos

# POST new todo for the authenticated user
@app.post("/todos", response_model=schemas.ToDo, status_code=status.HTTP_201_CREATED)
def add_todo(todo: schemas.ToDoCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    new_todo = crud.create_todo_item(db, todo, user_id=current_user.id)
    return new_todo

# PUT to toggle the completion status of a todo for the authenticated user
@app.put("/todos/{todo_id}", response_model=schemas.ToDo, status_code=status.HTTP_200_OK)
def toggle_todo(todo_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    todo = crud.toggle_todo_item(db, todo_id, user_id=current_user.id)
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ToDo item not found.")
    return todo

# DELETE todo for the authenticated user
@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    todo_deleted = crud.delete_todo_item(db, todo_id, user_id=current_user.id)
    if todo_deleted is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ToDo item not found.")
    return {"message": "ToDo item successfully deleted"}
