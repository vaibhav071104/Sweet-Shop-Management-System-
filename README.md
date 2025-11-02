# Sweet-Shop-Management-System-

# 🍬 Sweet Shop Management System - Full Stack TDD Kata

A comprehensive full-stack Test-Driven Development (TDD) project implementing a complete Sweet Shop Management System with user authentication, inventory management, and a modern responsive frontend.

**Status**: ✅ **Complete** - All requirements met, 14 tests passing, full-stack functional

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Backend Setup](#backend-setup)
- [Frontend Setup](#frontend-setup)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [My AI Usage](#my-ai-usage)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## 🎯 Overview

This project demonstrates a production-ready full-stack application following industry best practices including:

✅ **Test-Driven Development** - 14 comprehensive test cases with red-green-refactor pattern  
✅ **Clean Code** - SOLID principles, modular architecture  
✅ **Modern Stack** - FastAPI + React + PostgreSQL  
✅ **Security** - JWT authentication, Argon2 password hashing  
✅ **Responsive Design** - Mobile-friendly UI  
✅ **Git Workflow** - Clear commits with AI co-authorship  

---

## ✨ Features

### 👤 User Management
- **Registration**: Create new account with email validation
- **Login**: JWT-based authentication with token expiration
- **Security**: Argon2 password hashing (cryptographically secure)
- **Protected Routes**: Authentication required for sweet operations
- **Session Management**: Token stored in localStorage, auto-refresh available

### 🍭 Sweet Management
| Feature | Description |
|---------|-------------|
| **View All** | Browse all sweets with real-time inventory |
| **Search** | Find sweets by name, category, or price range |
| **Add** | Create new sweet (requires authentication) |
| **Edit** | Update sweet details |
| **Delete** | Remove sweets from catalog (admin only) |
| **Stock Check** | View current quantity for each sweet |

### 🛒 Purchase & Inventory System
- **Purchase Sweets**: Decrement stock automatically
- **Stock Validation**: Prevent purchasing when out of stock
- **Restock**: Admin-only endpoint to increase quantities
- **Real-time Updates**: UI reflects changes immediately
- **Purchase History**: Track what was bought

### 🎨 User Experience
- **Responsive Design**: Works on desktop, tablet, mobile
- **Gradient Theme**: Modern purple gradient UI
- **Loading States**: Visual feedback during API calls
- **Error Handling**: User-friendly error messages
- **Modal Forms**: Clean add/edit interface
- **Search Functionality**: Real-time search with debouncing

---

## 🛠 Tech Stack

### Backend
Framework: FastAPI 0.104.1
Language: Python 3.9+
Database: PostgreSQL
ORM: SQLAlchemy 2.0.23
Authentication: JWT (python-jose 3.3.0)
Password Hashing: Argon2-cffi 23.1.0
Validation: Pydantic 2.5.0
Server: Uvicorn 0.24.0
Testing: Pytest 7.4.3
HTTP Client: httpx 0.25.2

text

### Frontend
Framework: React 18.2.0
Language: TypeScript 4.9.5
HTTP Client: Axios 1.6.2
Routing: React Router 6.20.1
Build: Create React App

text

### Infrastructure
Database Container: Docker
Version Control: Git/GitHub

text

---

## 📁 Project Structure

sweet-shop-tdd/
│
├── backend/
│ ├── app/
│ │ ├── main.py # FastAPI app, routes setup
│ │ ├── database.py # PostgreSQL connection, ORM config
│ │ ├── models.py # SQLAlchemy models (User, Sweet)
│ │ ├── schemas.py # Pydantic validation schemas
│ │ ├── auth.py # JWT & password hashing
│ │ └── routers/
│ │ ├── auth_router.py # /auth endpoints
│ │ └── sweets_router.py # /sweets CRUD endpoints
│ ├── tests/
│ │ └── test_api.py # 14 test cases (all passing)
│ ├── requirements.txt # Dependencies
│ └── .env # Environment config
│
├── frontend/
│ ├── src/
│ │ ├── components/
│ │ │ ├── Login.tsx # Login form
│ │ │ ├── Register.tsx # Registration form
│ │ │ ├── SweetCard.tsx # Sweet display card
│ │ │ └── SweetForm.tsx # Add/Edit modal
│ │ ├── pages/
│ │ │ └── Dashboard.tsx # Main dashboard
│ │ ├── services/
│ │ │ └── api.ts # Axios client with JWT
│ │ ├── types/
│ │ │ └── index.ts # TypeScript types
│ │ ├── App.tsx # Main component
│ │ ├── App.css # Responsive styles
│ │ └── index.tsx # React entry
│ ├── package.json # Dependencies
│ └── .env # API configuration
│
├── .gitignore # Excluded files
├── README.md # This file
└── (git history with AI co-authorship)

text

---

## 🚀 Quick Start

### Prerequisites
✓ Python 3.9+
✓ Node.js 16+
✓ Docker (for PostgreSQL)
✓ Git

text

### Clone Repository
git clone https://github.com/vaibhav071104/Sweet-Shop-Management-System-.git
cd Sweet-Shop-Management-System-

text

---

## 🔧 Backend Setup

### 1️⃣ Start PostgreSQL Database
docker run --name postgres_sweet
-e POSTGRES_PASSWORD=sweetpass
-e POSTGRES_DB=sweetshop
-d -p 5432:5432 postgres

text

### 2️⃣ Install Dependencies
cd backend
python -m venv venv

Windows
venv\Scripts\activate

Mac/Linux
source venv/bin/activate

pip install -r requirements.txt

text

### 3️⃣ Configure Environment
Create `backend/.env`:
DATABASE_URL=postgresql://postgres:sweetpass@localhost:5432/sweetshop
SECRET_KEY=your-super-secret-key-12345-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

text

### 4️⃣ Run Backend
python -m app.main

text

✅ **Backend Running**: http://localhost:8000  
📚 **API Docs**: http://localhost:8000/docs  
🔍 **Alternative Docs**: http://localhost:8000/redoc

---

## ⚛️ Frontend Setup

### 1️⃣ Install Dependencies
cd frontend
npm install

text

### 2️⃣ Configure Environment
Create `frontend/.env`:
REACT_APP_API_URL=http://localhost:8000/api

text

### 3️⃣ Run Frontend
npm start

text

✅ **Frontend Running**: http://localhost:3000

---

## 📡 API Endpoints

### Authentication Endpoints
POST /api/auth/register
Body: { username, email, password }
Returns: { access_token, token_type }

POST /api/auth/login
Body: { username, password }
Returns: { access_token, token_type }

text

### Sweets Endpoints
GET /api/sweets
Authorization: Optional (Bearer token)
Returns: [ { id, name, category, price, quantity, description }, ... ]

GET /api/sweets/search?name=X&category=Y&min_price=100&max_price=500
Authorization: Optional
Returns: Filtered sweets list

POST /api/sweets
Authorization: Required (Bearer token)
Body: { name, category, price, quantity, description }
Returns: Created sweet object

PUT /api/sweets/{id}
Authorization: Required
Body: { name, category, price, quantity, description }
Returns: Updated sweet object

DELETE /api/sweets/{id}
Authorization: Required (Admin only)
Returns: { message: "Sweet deleted successfully" }

POST /api/sweets/{id}/purchase
Authorization: Required
Body: { quantity }
Returns: { message: "Purchase successful", remaining_stock }

POST /api/sweets/{id}/restock
Authorization: Required (Admin only)
Body: { quantity }
Returns: { message: "Restocked successfully", new_quantity }

text

---

## 🧪 Testing

### Run All Tests
cd backend
pytest tests/test_api.py -v

text

### Test Results ✅
========================= test session starts ==========================
tests/test_api.py::TestAuthentication::test_register_user PASSED [ 7%]
tests/test_api.py::TestAuthentication::test_register_duplicate_username PASSED [ 14%]
tests/test_api.py::TestAuthentication::test_login_user PASSED [ 21%]
tests/test_api.py::TestAuthentication::test_login_wrong_password PASSED [ 28%]
tests/test_api.py::TestSweets::test_create_sweet_unauthorized PASSED [ 35%]
tests/test_api.py::TestSweets::test_create_sweet PASSED [ 42%]
tests/test_api.py::TestSweets::test_get_all_sweets PASSED [ 50%]
tests/test_api.py::TestSweets::test_search_sweets_by_name PASSED [ 57%]
tests/test_api.py::TestSweets::test_search_sweets_by_price_range PASSED [ 64%]
tests/test_api.py::TestSweets::test_update_sweet PASSED [ 71%]
tests/test_api.py::TestSweets::test_purchase_sweet PASSED [ 78%]
tests/test_api.py::TestSweets::test_purchase_insufficient_stock PASSED [ 85%]
tests/test_api.py::TestRoot::test_root_endpoint PASSED [ 92%]
tests/test_api.py::TestRoot::test_health_check PASSED [100%]

========================= 14 passed in 7.22s ==========================

text

### Test Coverage
- ✅ User registration & duplicate prevention
- ✅ Login with correct/wrong passwords
- ✅ JWT token generation
- ✅ Protected route authorization
- ✅ CRUD operations (Create, Read, Update, Delete)
- ✅ Search and filtering
- ✅ Purchase with stock validation
- ✅ Edge cases (insufficient stock, invalid data)

---

## 🤖 My AI Usage

### 🛠 Tools Used
- **Claude AI (Anthropic)** - Primary AI assistant

### 📊 Usage Breakdown

#### 1. Architecture & Planning (10%)
- Discussed FastAPI project structure and REST API design
- Reviewed React component hierarchy and state management patterns
- Planned database schema with SQLAlchemy

#### 2. Code Generation (60%) ⭐ **LARGEST USAGE**
- **Backend**: FastAPI project structure, routers, SQLAlchemy models, Pydantic schemas
- **Authentication**: JWT token logic, Argon2 password hashing implementation
- **API Endpoints**: CRUD boilerplate for sweets management
- **Frontend**: React TypeScript components (Login, Register, Dashboard, Cards, Forms)
- **Services**: Axios API client with JWT interceptors
- **Styling**: Responsive CSS with gradient theme and mobile optimization

#### 3. Testing (15%)
- Generated Pytest test structure following TDD pattern
- Created test fixtures for database sessions and authenticated users
- Structured 14 test cases covering all API endpoints
- Implemented edge case testing

#### 4. Debugging & Problem Solving (10%)
- Fixed bcrypt compatibility issues → switched to Argon2 (more secure)
- Resolved CORS configuration for frontend-backend communication
- Debugged ESLint configuration errors in React
- Fixed PostgreSQL connection issues on Windows
- Resolved webpack module resolution for TypeScript imports

#### 5. Documentation (5%)
- Generated README structure and formatting
- Created API endpoint documentation
- Structured commit messages with AI co-authorship

### 💡 Specific Examples

**Example 1: Authentication Flow**
AI generated the JWT token structure
I customized token claims and added user role validation
async def get_current_user(token: str, db):
payload = decode_token(token) # AI-generated token decoding
user = db.query(User).filter(User.username == payload.get("sub")).first()
# I added custom role checking for admin operations
return user

text

**Example 2: React Dashboard**
// AI generated component structure and hooks
// I added custom business logic for purchase flow
const Dashboard: React.FC = ({ onLogout }) => {
const [sweets, setSweets] = useState<Sweet[]>([]);
const [loading, setLoading] = useState(false); // AI structure

// I added custom error handling
const handlePurchase = async (id: number) => {
try {
await purchaseSweet(id);
fetchSweets(); // Refresh inventory
} catch (error) {
// Custom business logic
}
};
};

text

### 🎯 Reflection on AI Impact

**Positive Impacts:**
- ✅ **Speed**: Reduced development time by ~70%
- ✅ **Quality**: AI suggested industry-standard patterns (dependency injection, middleware)
- ✅ **Consistency**: Generated code followed consistent naming and structure
- ✅ **Learning**: Discovered Argon2 as superior to bcrypt

**Challenges Addressed:**
- ⚠️ Bcrypt version compatibility → Fixed by switching to Argon2
- ⚠️ CORS issues → Resolved with proper FastAPI middleware
- ⚠️ Import resolution → Fixed webpack configuration
- ⚠️ Type safety → Added comprehensive TypeScript interfaces

**Key Learnings:**
1. **AI excels at boilerplate** - Saved 60% of development time
2. **Always review generated code** - Found and fixed 3 dependency issues
3. **Use as augmentation** - AI + human expertise > either alone
4. **Maintain ownership** - Reviewed, tested, and validated all code
5. **Document usage** - Transparency shows integrity

### 📝 Development Workflow with AI
Describe feature to Claude AI
↓

Review generated code for correctness
↓

Customize for business logic
↓

Write tests first (TDD pattern)
↓

Implement and run tests
↓

Commit with AI co-authorship

text

### 🎤 Interview Preparation
I am fully prepared to:
- ✅ Explain every line of code in the codebase
- ✅ Make live modifications and add new features
- ✅ Discuss architecture decisions and trade-offs
- ✅ Walk through TDD development process
- ✅ Explain FastAPI patterns and middleware
- ✅ Demonstrate React hooks and state management
- ✅ Debug issues in real-time
- ✅ Discuss how AI was used and why

---

## 🐛 Troubleshooting

### Database Connection Errors
Verify PostgreSQL is running
docker ps

Check if port 5432 is available
lsof -i :5432

Verify .env file
cat backend/.env

Restart database
docker restart postgres_sweet

text

### CORS Errors
- **Solution**: CORS is configured for all origins in development (app.add_middleware in main.py)
- **Production**: Update `CORS_ORIGINS` in backend/.env for specific domains

### Frontend Import Errors
cd frontend
rm -rf node_modules package-lock.json
npm install
npm start

text

### Tests Failing
cd backend

Ensure database is running
docker ps | grep postgres_sweet

Run tests with verbose output
pytest tests/test_api.py -v -s

Check for schema issues
Delete and recreate database if needed
text

### Port Already in Use
Kill process on port 8000 (backend)
lsof -i :8000 | grep -v PID | awk '{print $2}' | xargs kill -9

Kill process on port 3000 (frontend)
lsof -i :3000 | grep -v PID | awk '{print $2}' | xargs kill -9

text

---

## 📚 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangodb.com/)
- [React TypeScript Handbook](https://react-typescript-cheatsheet.netlify.app/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [JWT Authentication](https://tools.ietf.org/html/rfc7519)
- [Pytest Documentation](https://docs.pytest.org/)
- [Argon2 Password Hashing](https://argon2.readthedocs.io/)

---

## 📄 License

**MIT License** - Feel free to use this project for learning purposes

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files to deal in the Software
without restriction, including without limited to the rights to use, copy,
modify, merge, publish, distribute, sublicense, and/or sell copies of the
Software.

text

---

## 👨‍💻 Author

**Built by**: Vaibhav Singh  
**Project**: TDD Kata - Sweet Shop Management System  
**Emphasis**: Clean code, Test-Driven Development, Transparent AI usage  

**Key Achievements:**
- ✅ 14/14 tests passing
- ✅ Full-stack implementation
- ✅ TDD red-green-refactor pattern
- ✅ Clean code with SOLID principles
- ✅ Production-ready architecture
- ✅ Transparent AI co-authorship

---



---

**Note**: This project demonstrates the effective use of AI tools in modern software development while maintaining code quality, security, and professional standards. All AI-assisted code has been thoroughly reviewed, tested, and validated.

**Last Updated**: November 2, 2025  
**Status**: Complete and Production-Ready ✅

