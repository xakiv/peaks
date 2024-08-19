import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from ..config import settings
from ..database import Base
from ..main import app, get_db


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_TEST_DB}"

# Create a SQLAlchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    poolclass=StaticPool,
)

# Create a sessionmaker to manage sessions
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables in the database
Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a new database session with a rollback at the end of the test."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def test_client(db_session):
    """Create a test client that uses the override_get_db fixture to return a session."""

    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture()
def set_bbox_param():
    return {"bbox": "-2.526855,41.153842,3.328857,43.596306"}


@pytest.fixture()
def peak_one_payload():
    return {
        "name": "Col de Lizuniaga",
        "altitude": 220,
        "lon": -1.6260317910308506,
        "lat": 43.29751016605033,
    }


@pytest.fixture()
def peak_one_update_payload():
    return {
        "name": "Col de Lizuniaga",
        "altitude": 250,
        "lon": -1.6260317910308507,
        "lat": 43.29751016605034,
    }


@pytest.fixture()
def peak_two_payload():
    return {
        "name": "Col du Somport",
        "altitude": 1632,
        "lon": -0.5316565609282227,
        "lat": 42.80098698915395,
    }


@pytest.fixture()
def peak_three_payload():
    return {
        "name": "Mont Blanc",
        "altitude": 4805.59,
        "lon": 6.900000,
        "lat": 45.900000,
    }


def test_root(test_client):
    response = test_client.get("/api/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Deak hiker, this is the result of a technical assessment. "
    }


def test_create_peak(test_client, peak_one_payload):
    response = test_client.post("/api/peaks/", json=peak_one_payload)

    assert response.status_code == 201, response.text
    data = response.json()
    assert data["name"] == peak_one_payload["name"]
    assert data["altitude"] == peak_one_payload["altitude"]
    assert data["lon"] == peak_one_payload["lon"]
    assert data["lat"] == peak_one_payload["lat"]
    assert "id" in data
    peak_id = data["id"]

    response = test_client.get(f"/api/peaks/{peak_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == peak_one_payload["name"]
    assert data["altitude"] == peak_one_payload["altitude"]
    assert data["lon"] == peak_one_payload["lon"]
    assert data["lat"] == peak_one_payload["lat"]
    assert data["id"] == peak_id

    response = test_client.get("/api/peaks/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == peak_one_payload["name"]
    assert data[0]["altitude"] == peak_one_payload["altitude"]
    assert data[0]["lon"] == peak_one_payload["lon"]
    assert data[0]["lat"] == peak_one_payload["lat"]


def test_update_peak(test_client, peak_one_payload, peak_one_update_payload):
    response = test_client.post("/api/peaks/", json=peak_one_payload)
    assert response.status_code == 201, response.text
    peak_id = response.json()["id"]

    response = test_client.put(f"/api/peaks/{peak_id}", json=peak_one_update_payload)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == peak_one_update_payload["name"]
    assert data["altitude"] == peak_one_update_payload["altitude"]
    assert data["lon"] == peak_one_update_payload["lon"]
    assert data["lat"] == peak_one_update_payload["lat"]
    assert data["id"] == peak_id


def test_delete_peak(test_client, peak_one_payload):
    response = test_client.post("/api/peaks/", json=peak_one_payload)
    peak_id = response.json()["id"]

    response = test_client.delete(f"/api/peaks/{peak_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["detail"] == "Peak deleted"

    response = test_client.get(f"/api/peaks/{peak_id}")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Peak not found"

    response = test_client.delete(f"/api/peaks/{peak_id}")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Peak not found"


def test_filter_peak(
    test_client, peak_one_payload, peak_two_payload, peak_three_payload, set_bbox_param
):
    response = test_client.post("/api/peaks/", json=peak_one_payload)
    peak_one_id = response.json()["id"]
    response = test_client.post("/api/peaks/", json=peak_two_payload)
    peak_two_id = response.json()["id"]
    response = test_client.post("/api/peaks/", json=peak_three_payload)
    peak_three_id = response.json()["id"]

    response = test_client.get("/api/peaks/", params=set_bbox_param)
    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data) == 2, data

    ids = [row["id"] for row in data]
    assert peak_one_id in ids, data
    assert peak_two_id in ids, data
    assert peak_three_id not in ids, data
