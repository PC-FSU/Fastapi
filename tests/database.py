from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app

from app.config import settings
from app.database import get_db
from app.database import Base


# All of this code is moved to conftest.py which is default pytest file where defined fixture are available
# throughout the module. So in principle you don't need this.


# 🚀 Test database URL: because who wants to ruin production data?
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

# 🔧 Creating the test engine: the heart of our database operations
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 🧪 Magic session potion: used to brew database connections
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    """
    🧹 This fixture handles table cleanup like a pro:
    - Drops all existing tables (bye-bye data 👋)
    - Creates fresh new tables (hello shiny database! 🌟)
    """
    Base.metadata.drop_all(bind=engine)  # Out with the old
    Base.metadata.create_all(bind=engine)  # In with the new
    db = TestingSessionLocal()  # Summon a new database session
    try:
        yield db  # Here's your shiny new session! Use it wisely.
    finally:
        db.close()  # Don't forget to clean up after yourself! 🧽


@pytest.fixture()
def client(session):
    """
    🎮 Fixture for creating the test client:
    - Overrides the real database connection with our shiny test session
    """
    def override_get_db():
        """
        🛠️ Overrides FastAPI's get_db dependency with the test session.
        """
        try:
            yield session  # Use the test session like a boss
        finally:
            session.close()  # Good habits: always clean up! 🧹
    
    # 🔄 Dependency swap: real DB -> test DB
    app.dependency_overrides[get_db] = override_get_db

    # 🎉 Return the TestClient for making app requests
    yield TestClient(app)
