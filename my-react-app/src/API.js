

const BASE_URL = "http://localhost:8000/todos";

// Fetch all Todos from the FastAPI backend
export const fetchTodos = async () => {
  try {
    const response = await fetch(BASE_URL);
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching todos:", error);
    return [];
  }
};

// Add a new Todo
export const addTodo = async (newItem) => {
  try {
    const response = await fetch(BASE_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(newItem),
    });
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error adding todo:", error);
    return null;
  }
};

// Toggle Todo completion status
export const toggleTodo = async (id) => {
  try {
    const response = await fetch(`${BASE_URL}/${id}`, {
      method: "PUT",
    });
    const updatedTodo = await response.json();
    return updatedTodo;
  } catch (error) {
    console.error("Error toggling todo:", error);
    return null;
  }
};

// Delete Todo
export const deleteTodo = async (id) => {
  try {
    await fetch(`${BASE_URL}/${id}`, {
      method: "DELETE",
    });
    return true;
  } catch (error) {
    console.error("Error deleting todo:", error);
    return false;
  }
};
