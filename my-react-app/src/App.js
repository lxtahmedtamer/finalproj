// App.js
import { useRef, useState, useEffect } from "react";
import "./App.css";
import { fetchTodos, addTodo, toggleTodo, deleteTodo } from "./API"; // Import API functions

function App() {
  const [todos, setTodos] = useState([]);
  const inputRef = useRef();

  // Fetch all Todos when the component loads
  useEffect(() => {
    const getTodos = async () => {
      const data = await fetchTodos();
      console.log("Fetched Todos:", data); // Debug: Check what the API returns
      setTodos(Array.isArray(data) ? data : []); // Ensure the fetched data is an array
    };
    getTodos();
  }, []);

  // Add a new Todo
  const handleAddTodo = async () => {
    const text = inputRef.current.value;
    const newItem = { text, completed: false };
    const data = await addTodo(newItem);

    if (data) {
      setTodos([...todos, data]);  // Update the list with the new item
      inputRef.current.value = "";
    }
  };

  // Toggle Todo completion status
  const handleItemDone = async (id, index) => {
    const updatedTodo = await toggleTodo(id);

    if (updatedTodo) {
      const newTodos = [...todos];
      newTodos[index] = updatedTodo;
      setTodos(newTodos);
    }
  };

  // Delete Todo
  const handleDeleteItem = async (id, index) => {
    const success = await deleteTodo(id);

    if (success) {
      const newTodos = [...todos];
      newTodos.splice(index, 1);
      setTodos(newTodos);
    }
  };

  return (
    <div className="App">
      <h2>To Do List</h2>
      <div className="to-do-container">
        <ul>
          {(todos || []).map(({ id, text, completed }, index) => (
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
