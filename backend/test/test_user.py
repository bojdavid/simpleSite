from fastapi.testclient import TestClient  # For testing FastAPI endpoints
from app import schemas
from app.main import app
import pytest
from fastapi import status
from test.override_db import override_get_db


override_get_db()

client = TestClient(app)
token_data = ""

@pytest.mark.skip(reason="User already exists")
def test_create_user():
    """
        This functions tests the endpoint for creating a new user.
    """
    # Data for the new user
    data = {
        "fullname": "John Doe 54",
        "email": "johndoe54@example.com",
        "password": "securepassword123"
    }

    # Sending a POST request with form data
    response = client.post("/api/v1/adminAuth/signUp", data=data)

    # Print response for debugging
    print(response.status_code)
    print(response.json())

    # Assertions
    assert response.json()["email"] == data["email"], "Returned email does not match the input email."
    assert response.status_code == 200, "Expected status code 200 for successful user creation."
    assert "_id" in response.json(), "Response should contain the user's _id."
    assert "fullname" in response.json(), "Response should contain the user's fullname."
    assert "created_at" in response.json(), "Response should contain the user's created_at timestamp."
    assert "password" in response.json()
    assert "email" in response.json()
    assert "updated_at" in response.json()



def test_get_user():
    """
        This function test the endpoint for getting all users
    """
    response = client.get("/api/v1/adminAuth/")
    #for r in response.json():
    #    print(r)
    print(f"\nThere are {len(response.json())} users ")
    assert response.status_code == 200

#-----------TESTING THE LOGIN ENDPOINT----------
@pytest.fixture(scope="session")  # Or "session" for even broader scope - to make the returned value accessible by all tests functions in other files as well
def test_login():
    """
        This function tests the endpoint for logging in a user
    """
    data = { "username": "johndoe54@example.com", "password": "securepassword123"}
    response = client.post("/api/v1/adminAuth/login/", data=data)
    
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"

    try:
        token_data = response.json()
        token = schemas.Token(**token_data)  # Validate response with Token schema (if applicable)
        assert token.access_token is not None  # Check if access token exists
        assert token.token_type == "bearer"
        return token
    
    except Exception as e:
        print(f"Error parsing JSON: {e}")
        assert False, "Response is not valid JSON or does not match Token schema"




# ---------------------TESTING FOR POSSIBLE ERRORS DURING LOGIN-------------------

def test_login_incorrect_credentials():
    """Tests login with incorrect credentials (e.g., wrong password)."""
    login_data = {"username": "johndoe54@example.com", "password": "wrongpassword"}

    response = client.post("/api/v1/adminAuth/login", data=login_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "detail" in response.json()  # Check for an appropriate error message


def test_login_missing_email():
    """Tests login with missing email."""
    login_data = {"password": "securepassword123"}

    response = client.post("/api/v1/adminAuth/login", data=login_data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY  # or 422
    assert "detail" in response.json()  # Check for an appropriate error message


def test_login_missing_password():
    """Tests login with missing password."""
    login_data = {"username": "johndoe54@example.com"}

    response = client.post("/api/v1/adminAuth/login", data=login_data)
    #print(response.json())
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY  # or 422
    assert "detail" in response.json()  # Check for an appropriate error message

    

