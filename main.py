from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

import database
import models
import schemas

# Create database tables automatically if they don't exist yet
models.Base.metadata.create_all(bind=database.engine)

tags_metadata = [
    {
        "name": "Student Operations",
        "description": "Manage student records including create, read, update and delete operations.",
    },
]

app = FastAPI(
    title="Student Record Management API",
    description="A simple REST API for managing student records.",
    version="1.0.0",
    openapi_tags=tags_metadata,
    docs_url=None,
    redoc_url=None,
)

# Custom styled Swagger UI HTML template
SWAGGER_UI_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Student Record Management API - Docs</title>
    <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css">
    <style>
        /* Base page reset */
        body {
            margin: 0;
            padding: 0;
            background-color: #f3f4f6 !important;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
            color: #1e293b;
        }

        /* Top Navigation Bar */
        .custom-topbar {
            background-color: #181e29;
            border-bottom: 1px solid #2d3748;
            padding: 14px 36px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .custom-topbar .topbar-title {
            color: #ffffff;
            font-size: 15px;
            font-weight: 600;
            letter-spacing: 0.3px;
        }
        .custom-topbar .topbar-links a {
            color: #94a3b8;
            text-decoration: none;
            font-size: 14px;
            margin-left: 20px;
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
            transition: color 0.15s ease;
        }
        .custom-topbar .topbar-links a.active {
            color: #93c5fd;
            text-decoration: underline;
            text-underline-offset: 4px;
        }
        .custom-topbar .topbar-links a:hover {
            color: #ffffff;
        }

        /* Main Swagger UI Container */
        .swagger-ui {
            max-width: 1100px;
            margin: 0 auto;
            padding: 24px 36px 48px 36px;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        }

        .swagger-ui .topbar {
            display: none !important;
        }

        .swagger-ui .wrapper {
            padding: 0 !important;
        }

        /* Header Info Section */
        .swagger-ui .info {
            margin: 10px 0 24px 0 !important;
            border-bottom: 1px solid #e2e8f0 !important;
            padding-bottom: 20px !important;
        }
        .swagger-ui .info .title {
            font-size: 28px !important;
            font-weight: 700 !important;
            color: #0f172a !important;
            letter-spacing: -0.5px;
            margin-bottom: 6px !important;
            display: flex;
            align-items: center;
        }
        .swagger-ui .info p, .swagger-ui .info .description {
            font-size: 15px !important;
            color: #475569 !important;
            margin-top: 4px !important;
        }

        /* Badges */
        .swagger-ui .info .title small.version-stamp {
            background-color: #e2e8f0 !important;
            border-radius: 12px !important;
            padding: 3px 10px !important;
            margin-left: 10px !important;
            top: 0 !important;
        }
        .swagger-ui .info .title small.version-stamp pre.version {
            color: #475569 !important;
            font-size: 12px !important;
            font-weight: 600 !important;
            font-family: inherit !important;
            background: transparent !important;
            border: none !important;
            padding: 0 !important;
            margin: 0 !important;
        }

        /* Tag Section ("Student Operations") */
        .swagger-ui .opblock-tag-section {
            margin-top: 20px;
        }
        .swagger-ui .opblock-tag {
            border-bottom: none !important;
            padding: 12px 0 6px 0 !important;
            font-size: 20px !important;
            font-weight: 700 !important;
            color: #0f172a !important;
        }
        .swagger-ui .opblock-tag small {
            font-size: 14px !important;
            color: #64748b !important;
            font-weight: 400 !important;
            display: block;
            margin-top: 2px;
        }

        /* Operation Endpoint Cards */
        .swagger-ui .opblock {
            background: #252b37 !important;
            border: none !important;
            border-radius: 8px !important;
            box-shadow: none !important;
            margin: 0 0 10px 0 !important;
            overflow: hidden;
        }

        /* Operation Header Summary */
        .swagger-ui .opblock .opblock-summary {
            background: #252b37 !important;
            border: none !important;
            padding: 10px 16px !important;
            align-items: center;
        }

        /* Method Badges */
        .swagger-ui .opblock .opblock-summary-method {
            border-radius: 6px !important;
            font-weight: 700 !important;
            font-size: 12px !important;
            min-width: 62px !important;
            text-align: center !important;
            padding: 5px 10px !important;
            text-shadow: none !important;
            margin-right: 14px !important;
        }

        /* Muted Minimal Method Colors */
        .swagger-ui .opblock.opblock-get .opblock-summary-method {
            background: #86efac !important;
            color: #14532d !important;
        }
        .swagger-ui .opblock.opblock-post .opblock-summary-method {
            background: #93c5fd !important;
            color: #1e3a8a !important;
        }
        .swagger-ui .opblock.opblock-put .opblock-summary-method {
            background: #a5b4fc !important;
            color: #312e81 !important;
        }
        .swagger-ui .opblock.opblock-delete .opblock-summary-method {
            background: #fca5a5 !important;
            color: #881337 !important;
        }

        /* Path & Summary Typography */
        .swagger-ui .opblock .opblock-summary-path span,
        .swagger-ui .opblock .opblock-summary-path a {
            color: #ffffff !important;
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace !important;
            font-size: 15px !important;
            font-weight: 600 !important;
        }

        .swagger-ui .opblock .opblock-summary-description {
            color: #94a3b8 !important;
            font-size: 13px !important;
        }

        .swagger-ui .opblock .opblock-summary .authorization__btn svg,
        .swagger-ui .opblock .opblock-summary svg {
            fill: #94a3b8 !important;
        }

        /* Expanded Endpoint Body */
        .swagger-ui .opblock .opblock-body {
            background: #1e2430 !important;
            border-top: 1px solid #333b4d !important;
            padding: 20px !important;
        }

        .swagger-ui .opblock .opblock-section-header {
            background: transparent !important;
            box-shadow: none !important;
            padding: 8px 0 !important;
        }
        .swagger-ui .opblock .opblock-section-header h4 {
            color: #ffffff !important;
            font-size: 14px !important;
            font-weight: 600 !important;
        }

        .swagger-ui table thead tr td, 
        .swagger-ui table thead tr th {
            color: #94a3b8 !important;
            border-bottom: 1px solid #333b4d !important;
            font-size: 13px !important;
        }

        .swagger-ui .parameter__name {
            color: #e2e8f0 !important;
            font-weight: 600 !important;
        }

        .swagger-ui .parameter__type,
        .swagger-ui .parameter__deprecated,
        .swagger-ui .parameter__in {
            color: #94a3b8 !important;
        }

        .swagger-ui table.parameters td {
            color: #cbd5e1 !important;
            border-bottom: 1px solid #2d3546 !important;
        }

        .swagger-ui .response-col_status {
            color: #ffffff !important;
            font-weight: 600 !important;
        }
        .swagger-ui .response-col_description {
            color: #cbd5e1 !important;
        }
        .swagger-ui .response-col_links {
            color: #94a3b8 !important;
        }

        /* Try It Out & Execute Buttons */
        .swagger-ui .btn.try-it-out__btn {
            background: transparent !important;
            border: 1px solid #3b82f6 !important;
            color: #93c5fd !important;
            border-radius: 6px !important;
            font-size: 13px !important;
            padding: 5px 14px !important;
            box-shadow: none !important;
        }
        .swagger-ui .btn.try-it-out__btn:hover {
            background: rgba(59, 130, 246, 0.12) !important;
        }

        .swagger-ui .btn.execute {
            background: #3b82f6 !important;
            border: none !important;
            color: #ffffff !important;
            border-radius: 6px !important;
            font-weight: 600 !important;
            box-shadow: none !important;
            padding: 6px 18px !important;
        }

        .swagger-ui .btn.cancel {
            border-color: #ef4444 !important;
            color: #fca5a5 !important;
            background: transparent !important;
        }

        /* Code & JSON display areas */
        .swagger-ui pre,
        .swagger-ui .highlight-code,
        .swagger-ui .microlight {
            background: #161a23 !important;
            border: 1px solid #2d3546 !important;
            border-radius: 6px !important;
            color: #e2e8f0 !important;
        }
        .swagger-ui code {
            color: #e2e8f0 !important;
        }

        /* Form Inputs & Selects */
        .swagger-ui input[type=text],
        .swagger-ui textarea,
        .swagger-ui select {
            background: #161a23 !important;
            border: 1px solid #333b4d !important;
            color: #ffffff !important;
            border-radius: 6px !important;
            padding: 8px 10px !important;
        }

        /* Schemas Section */
        .swagger-ui .models {
            background: #e5e7eb !important;
            border: 1px solid #d1d5db !important;
            border-radius: 8px !important;
            padding: 16px !important;
            margin-top: 24px !important;
            box-shadow: none !important;
        }
        .swagger-ui .models h4 {
            color: #1e293b !important;
            font-size: 16px !important;
            font-weight: 600 !important;
            border-bottom: none !important;
        }
        .swagger-ui .models .model-container {
            background: #f3f4f6 !important;
            border-radius: 6px !important;
            margin: 8px 0 !important;
            border: 1px solid #e5e7eb !important;
        }
        .swagger-ui .model-title {
            color: #1e293b !important;
        }
    </style>
</head>
<body>
    <div class="custom-topbar">
        <span class="topbar-title">Student Record API</span>
        <div class="topbar-links">
            <a href="/docs" class="active">/docs</a>
            <a href="/openapi.json" target="_blank">/openapi.json</a>
        </div>
    </div>
    <div id="swagger-ui"></div>
    <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
    <script>
        window.onload = () => {
            window.ui = SwaggerUIBundle({
                url: '/openapi.json',
                dom_id: '#swagger-ui',
                deepLinking: true,
                presets: [
                    SwaggerUIBundle.presets.apis,
                    SwaggerUIBundle.SwaggerUIStandalonePreset
                ],
                layout: "BaseLayout"
            });
        };
    </script>
</body>
</html>
"""


@app.get("/docs", include_in_schema=False)
def custom_swagger_ui():
    return HTMLResponse(content=SWAGGER_UI_HTML)


@app.post(
    "/students",
    response_model=schemas.StudentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new student record",
    tags=["Student Operations"],
)
def create_student(
    student: schemas.StudentCreate, db: Session = Depends(database.get_db)
):
    """
    Create a new student with:
    - name: Student's name
    - roll_number: Unique roll number
    - department: Department name
    - year: Year of study (1-4)
    """
    existing_student = (
        db.query(models.Student)
        .filter(models.Student.roll_number == student.roll_number)
        .first()
    )
    if existing_student:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Roll number '{student.roll_number}' is already registered.",
        )

    new_student = models.Student(
        name=student.name,
        roll_number=student.roll_number,
        department=student.department,
        year=student.year,
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student


@app.get(
    "/students",
    response_model=List[schemas.StudentResponse],
    status_code=status.HTTP_200_OK,
    summary="Retrieve all student records",
    tags=["Student Operations"],
)
def get_all_students(db: Session = Depends(database.get_db)):
    """Retrieve all student records stored in SQLite database."""
    students = db.query(models.Student).all()
    return students


@app.get(
    "/students/{student_id}",
    response_model=schemas.StudentResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve a single student record by ID",
    tags=["Student Operations"],
)
def get_student_by_id(student_id: int, db: Session = Depends(database.get_db)):
    """Retrieve a single student record using their unique database ID."""
    student = (
        db.query(models.Student)
        .filter(models.Student.id == student_id)
        .first()
    )
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {student_id} not found.",
        )
    return student


@app.put(
    "/students/{student_id}",
    response_model=schemas.StudentResponse,
    status_code=status.HTTP_200_OK,
    summary="Update an existing student record",
    tags=["Student Operations"],
)
def update_student(
    student_id: int,
    updated_data: schemas.StudentUpdate,
    db: Session = Depends(database.get_db),
):
    """Update name, roll number, department, and year of an existing student."""
    student = (
        db.query(models.Student)
        .filter(models.Student.id == student_id)
        .first()
    )
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {student_id} not found.",
        )

    duplicate_roll = (
        db.query(models.Student)
        .filter(
            models.Student.roll_number == updated_data.roll_number,
            models.Student.id != student_id,
        )
        .first()
    )
    if duplicate_roll:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Roll number '{updated_data.roll_number}' is already registered to another student.",
        )

    student.name = updated_data.name
    student.roll_number = updated_data.roll_number
    student.department = updated_data.department
    student.year = updated_data.year

    db.commit()
    db.refresh(student)
    return student


@app.delete(
    "/students/{student_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a student record",
    tags=["Student Operations"],
)
def delete_student(student_id: int, db: Session = Depends(database.get_db)):
    """Delete a student record by ID."""
    student = (
        db.query(models.Student)
        .filter(models.Student.id == student_id)
        .first()
    )
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {student_id} not found.",
        )

    db.delete(student)
    db.commit()
    return {"message": f"Student with ID {student_id} deleted successfully."}
