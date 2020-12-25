from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from my_app.database import Base
from my_app.main import app, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_cars():
    response = client.get("/cars")
    assert isinstance(response.json(), list)
    assert response.status_code == 200


def test_post_existing_car():
    "Posts a car that exists in external API"
    response = client.post("/cars", json={
        "make": "Fiat",
        "model": "500"
    })
    assert response.status_code == 200

def test_get_single_car():
    response = client.get("/cars/1")
    assert response.json()["model"] == "500"
    assert response.status_code == 200
    # client.delete

def test_delete_single_car():
    response = client.delete("/cars/1")
    assert response.status_code == 200
    # check if successfully deleted:
    response = client.get("/cars/1")
    assert response.status_code == 404

def test_post_invalid_car():
    "Posts car that does not exist in external API/in wrong data format"
    # does not exist
    response = client.post("/cars", json={"make": "Fiat", "model": "126P"})
    assert response.status_code == 404
    # format is wrong
    response = client.post("/cars", json = {"make": "lk"})
    assert response.status_code == 422

def test_post_same_twice():
    response = client.post("/cars", json={"make": "Fiat", "model": "500X"})
    assert response.status_code == 200
    # assert that if record already exists, response is 400
    response = client.post("/cars", json={"make": "Fiat", "model": "500X"})
    assert response.status_code == 400
    #cleanup after test
    client.delete("/cars/1")

def test_rating():
    client.post("/cars", json={"make": "Fiat", "model": "500L"})
    client.post("/cars", json={"make": "Fiat", "model": "500"})
    response = client.get("/cars")
    client.put("/rate", json={"make": "Fiat", "model": "500L", "score": 4})
    client.put("/rate", json={"make": "Fiat", "model": "500L", "score": 3})
    client.put("/rate", json={"make": "Fiat", "model": "500", "score": 3})
    client.put("/rate", json={"make": "Fiat", "model": "500", "score": 1})
    client.put("/rate", json={"make": "Fiat", "model": "500", "score": 2})
    client.put("/rate", json={"make": "Fiat", "model": "500", "score": 1})
    # assert that the one which was rated more often is first, although its score is lower
    response = client.get("/popular")
    popular_car = response.json()[0]
    unpopular_car = response.json()[1]
    assert popular_car["average_rate"] < unpopular_car["average_rate"]
    assert unpopular_car["rates_number"] < popular_car["rates_number"]
    assert response.status_code == 200
    client.delete("/cars/1")
    client.delete("/cars/2")





