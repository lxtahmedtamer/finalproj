from pydantic import BaseModel

class ToDoBase(BaseModel):
    text: str
    completed: bool

class ToDoCreate(ToDoBase):
    pass

class ToDo(ToDoBase):
    id: int
    completed: bool

    class Config:
        orm_mode = True
