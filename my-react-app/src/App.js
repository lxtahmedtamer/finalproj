import { useRef, useState, useEffect } from "react";
import "./App.css";

function App() {
  const [todos, setTodos] = useState([]);
  const inputRef = useRef();

  // Fetch all Todos from the FastAPI backend
  const fetchTodos = async () => {
    try {
      const response = await fetch("http://localhost:8000/todos");
      const data = await response.json();
      setTodos(data);
    } catch (error) {
      console.error("Error fetching todos:", error);
    }
  };

  // Add a new Todo
  const handleAddTodo = async () => {
    const text = inputRef.current.value;
    const newItem = { text, completed: false };
    
    try {
      const response = await fetch("http://localhost:8000/todos", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(newItem),
      });
      const data = await response.json();
      setTodos([...todos, data]);  // Update the list with the new item
      inputRef.current.value = "";
    } catch (error) {
      console.error("Error adding todo:", error);
    }
  };

  // Toggle Todo completion status
  const handleItemDone = async (id, index) => {
    try {
      const response = await fetch(`http://localhost:8000/todos/${id}`, {
        method: "PUT",
      });
      const updatedTodo = await response.json();
      const newTodos = [...todos];
      newTodos[index] = updatedTodo;
      setTodos(newTodos);
    } catch (error) {
      console.error("Error toggling todo:", error);
    }
  };

  // Delete Todo
  const handleDeleteItem = async (id, index) => {
    try {
      await fetch(`http://localhost:8000/todos/${id}`, {
        method: "DELETE",
      });
      const newTodos = [...todos];
      newTodos.splice(index, 1);
      setTodos(newTodos);
    } catch (error) {
      console.error("Error deleting todo:", error);
    }
  };

  // Fetch todos when the component loads
  useEffect(() => {
    fetchTodos();
  }, []);

  return (
    <div className="App">
      <h2>To Do List</h2>
      <div className="to-do-container">
        <ul>
          {todos.map(({ id, text, completed }, index) => (
            <div className="item" key={id}>
              <li
                className={completed ? "done" : ""}
                onClick={() => handleItemDone(id, index)}
              >
                {text}
              </li>
              <span onClick={() => handleDeleteItem(id, index)} className="trash">
                ❌
              </span>
            </div>
          ))}
        </ul>
        <input ref={inputRef} placeholder="Enter item..." />
        <button onClick={handleAddTodo}>Add</button>
      </div>
    </div>
  );
}

export default App;
