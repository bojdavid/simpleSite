from fastapi.testclient import TestClient  # For testing FastAPI endpoints
from app.main import app  # Import your FastAPI app instance
from fastapi import status
from test.override_db import override_get_db
from .test_user import test_login   #fixture was imported and is workng.
import pytest

import base64

override_get_db()
# Tiny transparent PNG (1x1 pixel) encoded in base64
tiny_png_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="

# Decode the base64 string to bytes
tiny_png_bytes = base64.b64decode(tiny_png_base64)

client = TestClient(app)
services = [
    {
        "service": "Web Design",
        "description": "Creating beautiful and functional websites.",
        "image": tiny_png_base64,  # Example bytes data
        "isApproved": False,
    },
    {
        "service": "Mobile App Development",
        "description": "Building native mobile applications for iOS and Android.",
        "image": "image_data_2",
        "isApproved": False,
    },
    {
        "service": "SEO Optimization",
        "description": "Improving website visibility in search engines.",
        "isApproved": False,
    },
    {
        "service": "Content Marketing",
        "description": "Creating engaging content to attract and retain customers.",
        "image": "image_data_4",
        "isApproved": False,
    },
    {
        "service": "Social Media Management",
        "description": "Managing social media presence for businesses.",
        "isApproved": False,
    },
    {
        "service": "E-commerce Solutions",
        "description": "Developing online stores and e-commerce platforms.",
        "image": "image_data_6",
        "isApproved": False,
    },
    {
        "service": "Data Analytics",
        "description": "Analyzing data to provide insights and drive business decisions.",
        "isApproved": False,
    },
    {
        "service": "Cloud Computing Services",
        "description": "Providing cloud infrastructure and solutions.",
        "image": "image_data_8",
        "isApproved": False,
    },
    {
        "service": "Cybersecurity Services",
        "description": "Protecting businesses from cyber threats.",
        "isApproved": False,
    },
    {
        "service": "IT Consulting",
        "description": "Providing expert IT advice and guidance.",
        "image": "image_data_10",
        "isApproved": False,
    },
]


# TESTING THE GET ALL SERVICE ENDPOINT
def test_get_allService():
    response = client.get("/api/v1/services")
    print(f"\nNo of services is {len(response.json())}")
    """
    for service in response.json():
        print(f"Service {service["service"]} Image - {service["image"]}")
    """
    assert response.status_code == 200

# TESTING THE ENDPOINT FOR GETTING A SERVICE
def test_get_Aservice():
    response = client.get("/api/v1/services/678848df107bfb288da3aef3")
    assert response.status_code == 200


# TESTING THE ENDPOINT FOR CREATING A SERVICE
@pytest.mark.skip(reason="Data has been created")
@pytest.mark.parametrize("data", services)
def test_create_service(test_login, data):
   #set the jwt bearer token in the headers
    headers = {"Authorization": f"Bearer {test_login.access_token}"}
    
    response = client.post("/api/v1/services", json=data, headers=headers)
    #print(f"Service {response.json()["service"]} Image - {response.json()["image"]}")
    assert response.status_code == status.HTTP_201_CREATED


# TESTING THE ENDPOINT FOR APPROVING A SERVICE
def test_approve_service(test_login):
    #set the jwt bearer token in the headers
    headers = {"Authorization": f"Bearer {test_login.access_token}"}
    data = {"isApproved": False}
    response = client.put("/api/v1/services/approve/678848df107bfb288da3aeef", json=data, headers=headers)
    #print(response.json())
    assert response.status_code == status.HTTP_200_OK

# TESTING THE ENDPOINT FOR UPDATING A SERVICE
def test_update_service(test_login):
    headers = {"Authorization": f"Bearer {test_login.access_token}"}
    data = {
        "service": "Web Design and it has been updated",
        "description": "Creating beautiful and functional websites.",
        "image": tiny_png_base64,  # Example bytes data
        "isApproved": False,
    }
    response = client.put("/api/v1/services/678848df107bfb288da3aeef", json=data, headers=headers)
    #print(response.json())
    assert response.status_code == status.HTTP_200_OK


# TESTING THE ENDPOINT FOR DELETING A SERVICE
@pytest.mark.skip(reason="The service with this Id has already been deleted")
def test_delete_service(test_login):
    headers = {"Authorization": f"Bearer {test_login.access_token}"}
    response = client.delete("/api/v1/services/678848df107bfb288da3af01", headers=headers)
    
    #print(response.json(), response.status_code)
    assert response.status_code == 200


#---------------TESTING ENDPOINTS WITH FALSEUSER ID TO SEE THE RETURNED MESSAGE -----------

# TESTING DELETE ENDPOINT WITH A FALSEUSERID
def test_delete_falseUserId(test_login):
    headers = {"Authorization": f"Bearer {test_login.access_token}"}
    response = client.delete("/api/v1/services/678848df107bfb288da3af02", headers=headers)

    assert response.json()["detail"] == "Service not found"
    assert response.status_code == 404

# TESTING UPDATE ENDPOINT WITH A FALSEUSERID
def test_update_falseUserId(test_login):
    id = "678848df107bfb288da3af02"
    headers = {"Authorization": f"Bearer {test_login.access_token}"}
    data= {
        "service": "Web Design",
        "description": "Creating beautiful and functional websites.",
        "image": tiny_png_base64,  # Example bytes data
        "isApproved": False,
    }
    response = client.put(f"/api/v1/services/{id}", headers=headers, json=data)

    assert response.json()["detail"] ==  f"Service with id of {id} was not found"
    assert response.status_code == 404

# TESTING GETTING A SINGLE SERVICE WITH A FALSEUSERID
def test_get_falseUserId(test_login):
    headers = {"Authorization": f"Bearer {test_login.access_token}"}
    response = client.get("/api/v1/services/678848df107bfb288da3af02", headers=headers)

    assert response.json()["detail"] == "Service not found"
    assert response.status_code == 404

# TESTING APPROVAL ENDPOINT WITH A FALSE USERID
def test_approve_falseUserId(test_login):
    id = "678848df107bfb288da3af02"
    headers = {"Authorization": f"Bearer {test_login.access_token}"}
    data = {"isApproved":True}

    response = client.put(f"/api/v1/services/approve/{id}", headers=headers, json=data)

    assert response.json()["detail"] ==  f"service with id of {id} was not found"
    assert response.status_code == 404

