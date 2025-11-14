# GemConnect Backend - Project Nexus 🐍

## About GemConnect
GemConnect is a dynamic social media feed platform designed to connect users, allowing them to share posts, interact with content, and communicate in real-time. This repository contains the backend system, which manages user authentication, posts, comments, likes, shares, follows, notifications, and messaging through a scalable GraphQL API.

## Features
- User Management: Register, login, and maintain user profiles
- Post Management: Create, edit, and delete posts with optional images
- Commenting: Users can comment on posts with threaded interactions
- Likes: Track user likes for analytics and notifications
- Shares: Share posts with optional messages
- Follow System: Follow and unfollow users to curate feeds
- Notifications: Receive alerts for likes, comments, shares, follows, and messages
- Messaging: One-to-one chat between users with read status tracking
- GraphQL API: Flexible querying for posts, interactions, and users
- Database: PostgreSQL used for relational data storage
- Backend Framework: Django for rapid, secure backend development

## ERD (Entity Relationship Diagram)
The database schema for GemConnect is designed to ensure scalability and efficient relationships between entities.
![Application ERD](docs/images/GemConnect.png)


## Tech Stack
- Backend Framework: Django
- API: GraphQL (Graphene-Django)
- Database: PostgreSQL
- Authentication: Django Auth system
- Containerization: Docker (optional, for deployment)
- Testing: GraphQL Playground / Postman

<p align="left">
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django" />
  <img src="https://img.shields.io/badge/Graphene_Django-E10098?style=for-the-badge&logo=graphql&logoColor=white" alt="Graphene-Django" />
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL" />
  <img src="https://img.shields.io/badge/Django_Auth-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django Auth" />
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker" />
  <img src="https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white" alt="Postman" />
</p>

---

## Project Structure
```bash
gemconnect-backend/
├── gemconnect/         (Django project settings)
├── apps/               (All backend apps: users, posts, notifications, etc.)
├── manage.py           (Django CLI)
├── requirements.txt    (Python dependencies)
└── README.md           (This file)
```

## Installation (Beginner Friendly)

1.  **Clone the repository**
    ```bash
    git clone https://github.com/<your-username>/gemconnect-backend.git
    cd gemconnect-backend
    ```

2.  **Create and activate a virtual environment**
    ```bash
    # Create the environment
    python -m venv venv

    # Activate on Linux/Mac
    source venv/bin/activate

    # Activate on Windows
    venv\Scripts\activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables**
    * Create a `.env` file in the root directory.
    * Add your environment variables to this file. For example:

    ```.env
    SECRET_KEY=<your-secret-key>
    DATABASE_URL=postgres://user:password@localhost:5432/gemconnect_db
    ```

5.  **Run migrations**
    ```bash
    python manage.py migrate
    ```

6.  **Start the development server**
    ```bash
    python manage.py runserver
    ```

## Usage
- Access GraphQL Playground at http://127.0.0.1:8000/graphql/
- Test queries and mutations for users, posts, comments, likes, shares, follows, notifications, and messages

## Next Steps
- Implement real-time subscriptions for notifications and messaging (GraphQL Subscriptions / Channels)
- Write unit and integration tests
- Deploy backend (Docker / Heroku / Render)

## Collaboration & Contributions
This repository is for personal development as part of the ProDev Backend Engineering project. Collaborations or pull requests are welcome under mentorship guidelines.

## Roadmap
- Define data models and relationships
- Set up Django project
- Implement GraphQL API for posts, users, and interactions
- Implement authentication and permissions
- Connect to frontend apps (mobile & web)
- Deploy backend for live testing