import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_root_redirect():
    response = client.get("/", follow_redirects=False)
    # Should redirect with 307 or 302
    assert response.status_code in (302, 307)
    assert response.headers["location"].endswith("/static/index.html")

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_success():
    # Use a unique email to avoid duplicate
    response = client.post("/activities/Chess Club/signup", params={"email": "newstudent@mergington.edu"})
    assert response.status_code == 200
    assert "Signed up newstudent@mergington.edu for Chess Club" in response.json()["message"]

def test_signup_duplicate():
    # Try to sign up the same email again
    client.post("/activities/Programming Class/signup", params={"email": "unique@mergington.edu"})
    response = client.post("/activities/Programming Class/signup", params={"email": "unique@mergington.edu"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"

def test_signup_activity_not_found():
    response = client.post("/activities/Nonexistent/signup", params={"email": "ghost@mergington.edu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
