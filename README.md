
# LinkedIn Clone - Full Stack Application

A mini LinkedIn-like community platform built with Django REST Framework and React for CIAAN Cyber Tech Internship.

## 🚀 Features

- **User Authentication** (Register/Login)
- **User Profiles** with bio and profile information  
- **Post Feed** - Create and view text posts
- **Real-time Updates** - Posts appear instantly
- **Profile Pages** - View user profiles and their posts
- **Responsive Design** - Works on desktop and mobile

## 🛠️ Tech Stack

**Backend:**
- Django 5.2.2
- Django REST Framework
- SQLite Database
- Django CORS Headers

**Frontend:**
- React 18
- Axios for API calls
- Modern CSS with responsive design

## 📦 Project Structure

linkedin-clone/
├── backend/
│ ├── linkedin_backend/ # Django settings
│ ├── users/ # User authentication app
│ ├── posts/ # Posts and API views
│ └── manage.py
├── frontend/
│ └── linkedin-frontend/ # React application
└── README.md

text

## 🔧 Setup Instructions

### Backend Setup
cd backend
pip install django djangorestframework django-cors-headers
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

text

### Frontend Setup
cd frontend/linkedin-frontend
npm install
npm start

text

## 🌐 API Endpoints

- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `GET /api/posts/` - Get all posts
- `POST /api/posts/` - Create new post
- `GET /api/posts/user/{username}/` - Get user's posts
- `GET /api/profile/{username}/` - Get user profile

## 👤 Demo Users

After setup, create demo users for testing:
- Register through the UI at http://localhost:3000
- Or use Django admin at http://127.0.0.1:8000/admin/





