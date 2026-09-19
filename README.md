# Student Record Management REST API

A simple, beginner-friendly RESTful API built with **Python**, **FastAPI**, **SQLite**, and **SQLAlchemy** for managing student records.

## 📌 Project Overview

This API allows managing student records with full CRUD (Create, Read, Update, Delete) capabilities. It enforces data validation using Pydantic, persistent storage using SQLite via SQLAlchemy ORM, and auto-generates interactive API documentation via Swagger UI.

---

## ✨ Features

- **Create Student**: Add a new student record with unique roll numbers and validated academic year (1–4).
- **Read Students**: Fetch all student records or retrieve a single record by student ID.
- **Update Student**: Modify student details while maintaining roll number uniqueness.
- **Delete Student**: Remove a student record permanently.
- **Input Validation**: Automatic input validation and readable error messages (HTTP status codes 200, 201, 400, 404, 422).
- **Interactive Documentation**: Auto-generated Swagger documentation accessible at `/docs`.

---

## 🛠️ Technologies Used

- **Python 3.8+**
- **FastAPI**: Modern, high-performance web framework for building APIs.
- **SQLite**: Lightweight disk-based relational database.
- **SQLAlchemy**: Object-Relational Mapping (ORM) library.
- **Pydantic**: Data validation and settings management using Python type annotations.
- **Uvicorn**: Lightning-fast ASGI server implementation.

---

## 📁 Project Structure

```text
student-rest-api/
│
├── main.py           # FastAPI application and route handlers
├── database.py       # SQLite engine, session, and DB dependency setup
├── models.py         # SQLAlchemy database models
├── schemas.py        # Pydantic schemas for data validation
├── requirements.txt  # Project dependencies
└── README.md         # Project documentation
```

---

## ⚙️ Installation Instructions

1. **Navigate into the project directory:**
   ```bash
   cd student-rest-api
   ```

2. **(Optional) Create and activate a virtual environment:**
   - **On Windows:**
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   - **On macOS/Linux:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 How to Run the Project

Start the local server using Uvicorn:

```bash
uvicorn main:app --reload
```

The server will start at: `http://127.0.0.1:8000`

---

## 🔗 API Endpoints

| Method | Endpoint | Description | Success Code | Error Codes |
| :--- | :--- | :--- | :--- | :--- |
| **POST** | `/students` | Create a new student record | `201 Created` | `400 Bad Request`, `422 Unprocessable` |
| **GET** | `/students` | Get all student records | `200 OK` | - |
| **GET** | `/students/{id}` | Get student record by ID | `200 OK` | `404 Not Found` |
| **PUT** | `/students/{id}` | Update existing student record | `200 OK` | `400 Bad Request`, `404 Not Found`, `422 Unprocessable` |
| **DELETE** | `/students/{id}` | Delete student record | `200 OK` | `404 Not Found` |

---

## 📝 Example Request & Response JSON

### 1. Create Student (`POST /students`)
**Request Body:**
```json
{
  "name": "Alice Smith",
  "roll_number": "CS101",
  "department": "Computer Science",
  "year": 2
}
```

**Response (`201 Created`):**
```json
{
  "name": "Alice Smith",
  "roll_number": "CS101",
  "department": "Computer Science",
  "year": 2,
  "id": 1
}
```

---

### 2. Validation Rules & Errors

- **Year Constraint (`1` to `4`):**
  Sending `"year": 5` triggers a `422 Unprocessable Entity` response:
  ```json
  {
    "detail": [
      {
        "loc": ["body", "year"],
        "msg": "Input should be less than or equal to 4",
        "type": "less_than_equal"
      }
    ]
  }
  ```

- **Duplicate Roll Number:**
  Attempting to create another student with `"roll_number": "CS101"` triggers a `400 Bad Request` response:
  ```json
  {
    "detail": "Roll number 'CS101' is already registered."
  }
  ```

- **Student Not Found:**
  Requesting `GET /students/999` returns a `404 Not Found` response:
  ```json
  {
    "detail": "Student with ID 999 not found."
  }
  ```

---

## 🧪 How to Test Using FastAPI Swagger UI

1. Run the application (`uvicorn main:app --reload`).
2. Open your browser and go to: `http://127.0.0.1:8000/docs`.
3. Expand any API endpoint (e.g. `POST /students`).
4. Click **Try it out**.
5. Fill in the JSON request body and click **Execute**.
6. View the Response Body, Headers, and Status Code directly in the browser interface.
