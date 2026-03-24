from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List

app = FastAPI(title="Student Management API")


# 1. Data Model (Validation)

class Student(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    age: int = Field(..., gt=0, lt=100)
    course: str = Field(..., min_length=2, max_length=50)


# 2. In-memory Database

students_db = {}
student_id_counter = 1


# 3. GET /students

@app.get("/students", response_model=List[dict])
def get_students():
    return list(students_db.values())


# 4. POST /students

@app.post("/students", status_code=status.HTTP_201_CREATED)
def add_student(student: Student):
    global student_id_counter

    student_data = student.dict()
    student_data["id"] = student_id_counter

    students_db[student_id_counter] = student_data
    student_id_counter += 1

    return {
        "message": "Student added successfully",
        "student": student_data
    }


# 5. GET /students/{id}

@app.get("/students/{id}")
def get_student(id: int):
    if id not in students_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    return students_db[id]


# 6. PUT /students/{id}

@app.put("/students/{id}")
def update_student(id: int, updated_student: Student):
    if id not in students_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    student_data = updated_student.dict()
    student_data["id"] = id

    students_db[id] = student_data

    return {
        "message": "Student updated successfully",
        "student": student_data
    }


# 7. DELETE /students/{id}

@app.delete("/students/{id}")
def delete_student(id: int):
    if id not in students_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    del students_db[id]

    return {
        "message": "Student deleted successfully"
    }

def calculate_grade(score):
    if score >= 50:
        return "Pass"
    return "Fail"