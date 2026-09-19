import sys
from fastapi.testclient import TestClient
from main import app
import os

import database
import models

# Clear database tables to ensure clean test environment
db_session = database.SessionLocal()
models.Base.metadata.create_all(bind=database.engine)
db_session.query(models.Student).delete()
db_session.commit()
db_session.close()

client = TestClient(app)


def test_crud_and_validations():
    print("--- 1. Testing POST /students (Create Student) ---")
    response = client.post(
        "/students",
        json={
            "name": "John Doe",
            "roll_number": "CS101",
            "department": "Computer Science",
            "year": 1,
        },
    )
    print(f"Status: {response.status_code}, Body: {response.json()}")
    assert response.status_code == 201
    created_student = response.json()
    student_id = created_student["id"]
    assert created_student["name"] == "John Doe"
    assert created_student["roll_number"] == "CS101"
    assert created_student["year"] == 1

    print("\n--- 2. Testing POST /students Validation (Duplicate Roll Number) ---")
    duplicate_res = client.post(
        "/students",
        json={
            "name": "Jane Smith",
            "roll_number": "CS101",  # Same roll number
            "department": "Information Technology",
            "year": 2,
        },
    )
    print(f"Status: {duplicate_res.status_code}, Body: {duplicate_res.json()}")
    assert duplicate_res.status_code == 400
    assert "already registered" in duplicate_res.json()["detail"]

    print("\n--- 3. Testing POST /students Validation (Invalid Year = 5) ---")
    invalid_year_res = client.post(
        "/students",
        json={
            "name": "Jane Smith",
            "roll_number": "IT102",
            "department": "Information Technology",
            "year": 5,  # Invalid year (> 4)
        },
    )
    print(
        f"Status: {invalid_year_res.status_code}, Body: {invalid_year_res.json()}"
    )
    assert invalid_year_res.status_code == 422

    print("\n--- 4. Testing POST /students Validation (Invalid Year = 0) ---")
    invalid_year_res2 = client.post(
        "/students",
        json={
            "name": "Jane Smith",
            "roll_number": "IT102",
            "department": "Information Technology",
            "year": 0,  # Invalid year (< 1)
        },
    )
    print(
        f"Status: {invalid_year_res2.status_code}, Body: {invalid_year_res2.json()}"
    )
    assert invalid_year_res2.status_code == 422

    print("\n--- 5. Testing GET /students (Read All Students) ---")
    get_all_res = client.get("/students")
    print(f"Status: {get_all_res.status_code}, Body: {get_all_res.json()}")
    assert get_all_res.status_code == 200
    assert len(get_all_res.json()) == 1

    print("\n--- 6. Testing GET /students/{id} (Read Single Student) ---")
    get_one_res = client.get(f"/students/{student_id}")
    print(f"Status: {get_one_res.status_code}, Body: {get_one_res.json()}")
    assert get_one_res.status_code == 200
    assert get_one_res.json()["id"] == student_id

    print("\n--- 7. Testing GET /students/{id} (Non-existent ID) ---")
    get_not_found = client.get("/students/9999")
    print(f"Status: {get_not_found.status_code}, Body: {get_not_found.json()}")
    assert get_not_found.status_code == 404

    print("\n--- 8. Testing PUT /students/{id} (Update Student) ---")
    update_res = client.put(
        f"/students/{student_id}",
        json={
            "name": "Johnathan Doe",
            "roll_number": "CS101-UPDATED",
            "department": "Computer Science & Eng",
            "year": 2,
        },
    )
    print(f"Status: {update_res.status_code}, Body: {update_res.json()}")
    assert update_res.status_code == 200
    assert update_res.json()["name"] == "Johnathan Doe"
    assert update_res.json()["year"] == 2

    print("\n--- 9. Testing PUT /students/{id} (Non-existent ID) ---")
    update_not_found = client.put(
        "/students/9999",
        json={
            "name": "Ghost",
            "roll_number": "G000",
            "department": "None",
            "year": 1,
        },
    )
    print(
        f"Status: {update_not_found.status_code}, Body: {update_not_found.json()}"
    )
    assert update_not_found.status_code == 404

    print("\n--- 10. Testing DELETE /students/{id} (Delete Student) ---")
    delete_res = client.delete(f"/students/{student_id}")
    print(f"Status: {delete_res.status_code}, Body: {delete_res.json()}")
    assert delete_res.status_code == 200

    print("\n--- 11. Testing DELETE /students/{id} (Non-existent ID) ---")
    delete_not_found = client.delete("/students/9999")
    print(
        f"Status: {delete_not_found.status_code}, Body: {delete_not_found.json()}"
    )
    assert delete_not_found.status_code == 404

    print(
        "\n--- 12. Testing GET /students after deletion (Empty List) ---"
    )
    get_all_empty = client.get("/students")
    print(
        f"Status: {get_all_empty.status_code}, Body: {get_all_empty.json()}"
    )
    assert get_all_empty.status_code == 200
    assert len(get_all_empty.json()) == 0

    print("\n=== ALL TESTS PASSED SUCCESSFULLY! ===")


if __name__ == "__main__":
    test_crud_and_validations()
