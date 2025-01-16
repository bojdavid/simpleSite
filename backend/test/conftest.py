import pytest
import jwt
from .test_user import test_login 
from app.config import Settings

@pytest.fixture(scope="module")
def get_userCredentials(test_login):
    decoded_token = jwt.decode( jwt=test_login.access_token, algorithms=Settings.algorithm, key=Settings.secret_key)
    userId = decoded_token["userId"]
    name = decoded_token["name"]
    email = decoded_token["sub"]

    return {"userId":userId, "name":name, "email":email, "token":test_login.access_token}