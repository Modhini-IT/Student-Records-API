from sqlalchemy import Column, Integer, String
from database import Base


class Student(Base):
    """SQLAlchemy model representing the 'students' table in SQLite."""

    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    roll_number = Column(String, unique=True, index=True, nullable=False)
    department = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
