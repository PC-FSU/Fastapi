"""
conftest.py:
This file is a special configuration file for pytest. 
It provides shared fixtures and configurations for tests in the directory or subdirectories. 
Fixtures defined here are automatically discoverable by pytest, meaning no need to explicitly import them into test files. 🚀

Purpose:
- To set up reusable fixtures, like test database sessions or clients.
- To centralize common testing logic, keeping individual test files clean and focused.
"""

from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.config import settings
from app.database import get_db
from app.database import Base
from app.oauth2 import create_access_token
from app import ORM_models

# 🎉 Configuration for the test database: safely isolated from production
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

# 🔧 Create a database engine specifically for testing
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 🧪 Testing session factory: builds fresh database sessions for tests
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def session():
    """
    🧹 Session Fixture:
    - Drops all tables (cleanup) and recreates them for a fresh start.
    - Provides a test database session.
    """
    print("my session fixture ran")  # Debug message to track when the session fixture is used
    Base.metadata.drop_all(bind=engine)  # Clean slate!
    Base.metadata.create_all(bind=engine)  # Rebuild schema
    db = TestingSessionLocal()  # Create a new database session
    try:
        yield db  # Give the session to the test
    finally:
        db.close()  # Always clean up! 🧽

@pytest.fixture()
def client(session):
    """
    🎮 Client Fixture:
    - Overrides the app's `get_db` dependency to use the test database session.
    - Provides a test client for making requests to the FastAPI app.
    """
    def override_get_db():
        try:
            yield session  # Use the test database session
        finally:
            session.close()  # Cleanup after each test
    app.dependency_overrides[get_db] = override_get_db  # Swap out the real DB for the test DB
    yield TestClient(app)  # Return the test client

@pytest.fixture
def test_user(client):
    """
    🧍 Test User Fixture:
    - Creates a user for testing purposes.
    - Returns the created user's details.
    """
    user_data = {"email": "sanjeev@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)  # Create user via API
    assert res.status_code == 201  # Ensure user creation succeeded
    new_user = res.json()  # Parse the response
    new_user['password'] = user_data['password']  # Include plaintext password for convenience
    return new_user

@pytest.fixture
def test_user2(client):
    """
    🧍‍♀️ Secondary Test User Fixture:
    - Same as `test_user`, but for a second user. Because why test with one user when you can test with two? 🤷
    """
    user_data = {"email": "sanjeev123@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    """
    🔑 Token Fixture:
    - Generates an access token for the test user.
    """
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    """
    🛡️ Authorized Client Fixture:
    - Adds an authorization header to the test client.
    - Mimics a logged-in user making requests.
    """
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client

@pytest.fixture
def test_posts(test_user, session, test_user2):
    """
    📝 Test Posts Fixture:
    - Creates multiple posts for testing, associated with two different users.
    - Returns the created posts.
    """
    posts_data = [
        {"title": "first title", "content": "first content", "owner_id": test_user['id']},
        {"title": "2nd title", "content": "2nd content", "owner_id": test_user['id']},
        {"title": "3rd title", "content": "3rd content", "owner_id": test_user['id']},
        {"title": "3rd title", "content": "3rd content", "owner_id": test_user2['id']}
    ]

    def create_post_model(post):
        return ORM_models.Post(**post)  # Convert dict to Post model instance

    posts = list(map(create_post_model, posts_data))  # Transform posts data into Post objects
    session.add_all(posts)  # Add all posts to the session
    session.commit()  # Commit the transaction
    return session.query(ORM_models.Post).all()  # Return all created posts
