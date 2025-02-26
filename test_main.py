import pytest
from fastapi.testclient import TestClient
from main import app
from database import engine, SessionLocal
from models import Base
from sqlalchemy.orm import Session

@pytest.fixture
def client():
    Base.metadata.drop_all(bind=engine)  # Reset DB for tests
    Base.metadata.create_all(bind=engine)
    return TestClient(app)

@pytest.fixture
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_create_product(client):
    response = client.post("/products/", json={"name": "T-Shirt", "description": "Cotton", "price": 19.99, "stock": 100})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "T-Shirt"
    assert data["id"] == 1

def test_read_product(client):
    client.post("/products/", json={"name": "T-Shirt", "description": "Cotton", "price": 19.99, "stock": 100})
    response = client.get("/products/1")
    assert response.status_code == 200
    assert response.json()["name"] == "T-Shirt"

def test_update_stock(client):
    client.post("/products/", json={"name": "T-Shirt", "description": "Cotton", "price": 19.99, "stock": 100})
    response = client.patch("/products/1/stock", json={"quantity": 10})
    assert response.status_code == 200
    assert response.json()["stock"] == 90

def test_search_products(client):
    client.post("/products/", json={"name": "T-Shirt", "description": "Cotton", "price": 19.99, "stock": 100})
    response = client.get("/products/?name=shirt")
    assert response.status_code == 200
    assert len(response.json()) == 1