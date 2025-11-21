# GemConnect Backend API 🐍

[![Deployed on Render](https://img.shields.io/badge/Deployed_on-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://gemconnect-backend.onrender.com/admin/)
[![GraphQL API](https://img.shields.io/badge/API-GraphQL-E10098?style=for-the-badge&logo=graphql&logoColor=white)](https://gemconnect-backend.onrender.com/graphql/)
[![Built With Django](https://img.shields.io/badge/Built_With-Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)

## 📖 About GemConnect
**GemConnect** is a full-stack social media platform designed for creators to share portfolio work in a distraction-free environment. This repository hosts the **Backend API**, which powers the mobile application by managing authentication, social graph relationships, and content delivery.

It uses a **Monolithic Architecture** serving a **GraphQL API**, ensuring the frontend fetches exactly the data it needs in a single request.

## 🚀 Live Links
- **Live Admin Panel:** [https://gemconnect-backend.onrender.com/admin/](https://gemconnect-backend.onrender.com/admin/)
- **GraphiQL Playground:** [https://gemconnect-backend.onrender.com/graphql/](https://gemconnect-backend.onrender.com/graphql/)
- **Frontend Repository:** [Link to your Mobile Repo]

---

## 🛠 Tech Stack

| Category | Technology | Purpose |
| :--- | :--- | :--- |
| **Framework** | **Django** | Robust, secure web framework for rapid development. |
| **API** | **Graphene-Django** | Implements GraphQL schemas, queries, and mutations. |
| **Database** | **PostgreSQL** | Relational database for production (Hosted on Render). |
| **Auth** | **JSON Web Tokens (JWT)** | Stateless authentication via `django-graphql-jwt`. |
| **Hosting** | **Render** | Containerized cloud deployment. |
| **Server** | **Gunicorn & WhiteNoise** | Production server and static file management. |

---

## ⚡ Key Features

### 🔐 Authentication & Security
- **JWT Implementation:** Secure login/registration returning persistent tokens.
- **Middleware Protection:** Custom settings to handle CORS and Trusted Origins for mobile connectivity.

### 📡 Social Graph API
- **User Profiles:** Dynamic fetching of bio, avatar, follower/following counts.
- **Feed Logic:** Retrieval of posts sorted by recency with nested author details.
- **Interactions:** - **Mutations:** `createPost`, `likePost`, `createComment`, `followUser`.
  - **Optimized Queries:** `allPosts`, `user(id)`, `myNotifications`.

### 🖼️ Image Handling
- **Base64 Decoding:** Custom logic to accept raw image strings from mobile devices and convert them into Django `ContentFile` objects for storage.

---

## 🗂 Database Schema (ERD)
The database uses a relational model linking Users to their Content and Interactions.
![Application ERD](docs/images/GemConnect.png)


## 💻 Local Installation Guide

Follow these steps to run the backend locally for development.

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/gemconnect-backend.git
cd gemconnect-backend
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
The project defaults to **SQLite** for local development — no complex setup required.  
*Optional:* To test with the production setup, set `DEBUG=False` in `settings.py`.

### 5. Run Migrations & Server
```bash
python manage.py migrate
python manage.py runserver
```

The API will be available at:  
`http://127.0.0.1:8000/graphql/`

---

## 🧪 API Documentation (GraphQL)

You can test the API using the **GraphiQL Playground**.

### Sample Query: Fetch Feed
```graphql
query {
  allPosts {
    id
    content
    image
    author {
      username
      avatar
    }
    likes {
      id
    }
  }
}
```

### Sample Mutation: Login
```graphql
mutation {
  tokenAuth(username: "Matilda", password: "password123") {
    token
  }
}
```

---

## 🤝 Contributing
This project was built as a **Capstone Project / Project Nexus** for the **ProDev Engineering Program**.  
Developed by **Matilda Esenam Gbeve**.

---