from pydantic import BaseModel, Field, ConfigDict


class StudentBase(BaseModel):
    """Base Pydantic model for student data validation."""

    name: str = Field(..., min_length=1, description="Full name of the student")
    roll_number: str = Field(..., min_length=1, description="Unique roll number assigned to the student")
    department: str = Field(..., min_length=1, description="Department name (e.g. Computer Science)")
    year: int = Field(..., ge=1, le=4, description="Academic year (must be between 1 and 4)")


class StudentCreate(StudentBase):
    """Schema used when creating a new student record."""

    pass


class StudentUpdate(StudentBase):
    """Schema used when updating an existing student record."""

    pass


class StudentResponse(StudentBase):
    """Schema used for returning student details in responses."""

    id: int

    model_config = ConfigDict(from_attributes=True)
