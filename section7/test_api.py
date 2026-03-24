from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# Fixture (Reusable Data)

import pytest

@pytest.fixture
def sample_student():
    return {
        "name": "Ayush",
        "age": 21,
        "course": "CS"
    }


# Test: Create Student

def test_create_student(sample_student):
    response = client.post("/students", json=sample_student)

    assert response.status_code == 201
    assert "student" in response.json()


# Test: Get Students

def test_get_students():
    response = client.get("/students")

    assert response.status_code == 200
    assert isinstance(response.json(), list)