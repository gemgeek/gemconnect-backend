# GemConnect Backend - Project Nexus

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

## Project Structure
```bash
gemconnect-backend/
├── gemconnect/         (Django project settings)
├── apps/               (All backend apps: users, posts, notifications, etc.)
├── manage.py           (Django CLI)
├── requirements.txt    (Python dependencies)
└── README.md           (This file)
```

The problem is that the code commands are not inside proper Markdown code blocks. Markdown is very sensitive to indentation and spacing.

When you have a numbered list and want to put a code block inside a list item, the code block (starting with ```) must be indented.

Here is the corrected, copy-pasteable version.

The Correct Markdown
Markdown

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