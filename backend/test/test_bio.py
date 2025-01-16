from fastapi.testclient import TestClient  # For testing FastAPI endpoints
from app.main import app  # Import your FastAPI app instance
from fastapi import status
from test.override_db import override_get_db
from .test_user import test_login   #fixture was imported and is workng.
import pytest
from app.config import Settings

import jwt

override_get_db()
client = TestClient(app)

#@pytest.mark.skip(reason="No bio has been created yet")
def test_get_bio(test_login, get_userCredentials):
    #set the jwt bearer token in the headers
    id = ""
    headers = {"Authorization": f"Bearer {test_login.access_token}"}
    
    response = client.get(f"/api/v1/bio/{get_userCredentials["userId"]}", headers=headers)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.skip(reason="Bio has been created")
def test_create_Bio(test_login, get_userCredentials):
    userId = get_userCredentials["userId"]
    name = get_userCredentials["name"]
    email = get_userCredentials["email"]

    headers = {"Authorization": f"Bearer {get_userCredentials["token"]}"}
    data = {"name":name, "email":email, "description":"description",  "about":"this is about"}
    response = client.post(f"/api/v1/bio/{userId}", json=data,headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert "userId" in response.json()

def test_update_Bio(get_userCredentials):
    name = get_userCredentials["name"]
    email = get_userCredentials["email"]
    userId=get_userCredentials["userId"]
    bioId="678870969ac2b695f417e96f"

    headers = {"Authorization": f"Bearer {get_userCredentials["token"]}"}
    data = {"name":name, "email":email, "description":"description updated",  "about":"this is about updated"}
    response = client.put(f"/api/v1/bio/{bioId}", json=data,headers=headers)
    print(response.json())
    assert response.status_code == status.HTTP_200_OK
    assert "userId" in response.json()