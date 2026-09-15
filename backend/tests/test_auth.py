import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.main import app
from app.database import Base, get_db

# Use an isolated in-memory SQLite database with StaticPool for test isolation
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_register_and_login_flow(client):
    # 1. Register
    payload = {
        "email": "student1@edumind.edu",
        "full_name": "Priyanshu Student",
        "password": "mypassword123"
    }
    res_reg = client.post("/auth/register", json=payload)
    assert res_reg.status_code == 201
    data = res_reg.json()
    assert "access_token" in data
    assert data["user"]["email"] == "student1@edumind.edu"
    assert data["user"]["full_name"] == "Priyanshu Student"

    # 2. Duplicate registration should fail
    res_dup = client.post("/auth/register", json=payload)
    assert res_dup.status_code == 400
    assert "already exists" in res_dup.json()["detail"]

    # 3. Login with correct password
    res_login = client.post("/auth/login", json={
        "email": "student1@edumind.edu",
        "password": "mypassword123"
    })
    assert res_login.status_code == 200
    token = res_login.json()["access_token"]
    assert token

    # 4. Login with wrong password
    res_bad_login = client.post("/auth/login", json={
        "email": "student1@edumind.edu",
        "password": "wrongpassword"
    })
    assert res_bad_login.status_code == 401

    # 5. Access /auth/me with valid Bearer token
    res_me = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert res_me.status_code == 200
    profile = res_me.json()
    assert profile["email"] == "student1@edumind.edu"
    assert profile["full_name"] == "Priyanshu Student"

    # 6. Access /auth/me without token should fail
    res_unauth = client.get("/auth/me")
    assert res_unauth.status_code == 401
