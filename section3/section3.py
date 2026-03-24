from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session
# database setup
DATABASE_URL = "sqlite:///./students.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# db model
class StudentDB(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    course = Column(String)

# Create table
Base.metadata.create_all(bind=engine)

# pydantic schema
class Student(BaseModel):
    name: str
    age: int
    course: str

# dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#  fast-api app
app = FastAPI()

# create student
@app.post("/students")
def create_student(student: Student, db: Session = Depends(get_db)):
    db_student = StudentDB(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return {"student": db_student}

# get all students
@app.get("/students")
def get_students(db: Session = Depends(get_db)):
    return db.query(StudentDB).all()

# get by id
@app.get("/students/{id}")
def get_student(id: int, db: Session = Depends(get_db)):
    student = db.query(StudentDB).filter(StudentDB.id == id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# UPDATE Student

@app.put("/students/{id}")
def update_student(id: int, updated: Student, db: Session = Depends(get_db)):
    student = db.query(StudentDB).filter(StudentDB.id == id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    student.name = updated.name
    student.age = updated.age
    student.course = updated.course

    db.commit()
    return {"message": "Updated successfully", "student": student}


# DELETE Student

@app.delete("/students/{id}")
def delete_student(id: int, db: Session = Depends(get_db)):
    student = db.query(StudentDB).filter(StudentDB.id == id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    db.delete(student)
    db.commit()
    return {"message": "Deleted successfully"}

# SEARCH by Name

@app.get("/students/search/")
def search_students(name: str, db: Session = Depends(get_db)):
    results = db.query(StudentDB).filter(StudentDB.name.contains(name)).all()
    return results