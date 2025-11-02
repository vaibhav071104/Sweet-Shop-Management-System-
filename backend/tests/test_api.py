import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db
from app.models import User, Sweet

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# Test data
test_user = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123"
}

test_admin = {
    "username": "adminuser",
    "email": "admin@example.com",
    "password": "adminpass123"
}

test_sweet = {
    "name": "Chocolate Bar",
    "category": "Chocolate",
    "price": 2.99,
    "quantity": 100,
    "description": "Delicious milk chocolate"
}

class TestAuthentication:
    """Test authentication endpoints"""
    
    def test_register_user(self):
        """Test user registration"""
        response = client.post("/api/auth/register", json=test_user)
        assert response.status_code == 201
        assert "access_token" in response.json()
        assert response.json()["token_type"] == "bearer"
    
    def test_register_duplicate_username(self):
        """Test registering with duplicate username"""
        response = client.post("/api/auth/register", json=test_user)
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"]
    
    def test_login_user(self):
        """Test user login"""
        response = client.post("/api/auth/login", json={
            "username": test_user["username"],
            "password": test_user["password"]
        })
        assert response.status_code == 200
        assert "access_token" in response.json()
    
    def test_login_wrong_password(self):
        """Test login with wrong password"""
        response = client.post("/api/auth/login", json={
            "username": test_user["username"],
            "password": "wrongpassword"
        })
        assert response.status_code == 401

class TestSweets:
    """Test sweet management endpoints"""
    
    @pytest.fixture
    def auth_token(self):
        """Get authentication token"""
        response = client.post("/api/auth/login", json={
            "username": test_user["username"],
            "password": test_user["password"]
        })
        return response.json()["access_token"]
    
    def test_create_sweet_unauthorized(self):
        """Test creating sweet without authentication"""
        response = client.post("/api/sweets", json=test_sweet)
        assert response.status_code == 403
    
    def test_create_sweet(self, auth_token):
        """Test creating a sweet with authentication"""
        response = client.post(
            "/api/sweets",
            json=test_sweet,
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 201
        assert response.json()["name"] == test_sweet["name"]
    
    def test_get_all_sweets(self):
        """Test getting all sweets (public endpoint)"""
        response = client.get("/api/sweets")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_search_sweets_by_name(self):
        """Test searching sweets by name"""
        response = client.get("/api/sweets/search?name=Chocolate")
        assert response.status_code == 200
        assert len(response.json()) > 0
    
    def test_search_sweets_by_price_range(self):
        """Test searching sweets by price range"""
        response = client.get("/api/sweets/search?min_price=1&max_price=5")
        assert response.status_code == 200
    
    def test_update_sweet(self, auth_token):
        """Test updating a sweet"""
        # First create a sweet
        create_response = client.post(
            "/api/sweets",
            json=test_sweet,
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        sweet_id = create_response.json()["id"]
        
        # Update the sweet
        update_data = {"price": 3.99}
        response = client.put(
            f"/api/sweets/{sweet_id}",
            json=update_data,
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        assert response.json()["price"] == 3.99
    
    def test_purchase_sweet(self, auth_token):
        """Test purchasing a sweet"""
        # Get first sweet
        sweets = client.get("/api/sweets").json()
        if sweets:
            sweet_id = sweets[0]["id"]
            initial_quantity = sweets[0]["quantity"]
            
            response = client.post(
                f"/api/sweets/{sweet_id}/purchase",
                json={"quantity": 1},
                headers={"Authorization": f"Bearer {auth_token}"}
            )
            assert response.status_code == 200
            assert response.json()["remaining_stock"] == initial_quantity - 1
    
    def test_purchase_insufficient_stock(self, auth_token):
        """Test purchasing more than available stock"""
        sweets = client.get("/api/sweets").json()
        if sweets:
            sweet_id = sweets[0]["id"]
            
            response = client.post(
                f"/api/sweets/{sweet_id}/purchase",
                json={"quantity": 99999},
                headers={"Authorization": f"Bearer {auth_token}"}
            )
            assert response.status_code == 400
            assert "Insufficient stock" in response.json()["detail"]

class TestRoot:
    """Test root endpoints"""
    
    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        assert "Sweet Shop" in response.json()["message"]
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
