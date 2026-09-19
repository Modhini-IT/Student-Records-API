import database
import models

# Ensure tables exist
models.Base.metadata.create_all(bind=database.engine)

db = database.SessionLocal()

# Clear existing records
db.query(models.Student).delete()
db.commit()

# Insert sample students
sample_students = [
    models.Student(name="Arun Kumar", roll_number="CS2001", department="Computer Science", year=1),
    models.Student(name="Priya Sharma", roll_number="EC2002", department="Electronics & Comm", year=2),
    models.Student(name="Vijay Shankar", roll_number="ME2003", department="Mechanical Eng", year=3),
    models.Student(name="Ananya Roy", roll_number="IT2004", department="Information Tech", year=4),
]

for s in sample_students:
    db.add(s)

db.commit()
print("Successfully seeded 4 sample student records into students.db!")
db.close()
