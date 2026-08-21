# GlucoSense

> AI-powered diabetes risk awareness and health management platform.

GlucoSense is a web-based health platform designed to help users better understand and manage their metabolic health. The platform combines health assessments, medical profile management, health tracking, educational resources, doctor recommendations, and an AI-powered medical assistant in a single application.

GlucoSense is intended for health education and risk awareness purposes and does not replace professional medical diagnosis or treatment.

---

## Features

### Health Risk Assessment

Users can complete a health assessment and receive a diabetes risk evaluation.

* Risk score calculation
* Risk level classification
* Assessment history
* Detailed assessment reports
* Risk trend visualization
* Dynamic risk status indicators

### Medical Profile

Users can manage their personal health information through their medical profile.

Supported information includes:

* Full name
* Email
* Date of birth
* Diabetes type
* Weight
* Target blood glucose range

### Health Tracking

GlucoSense provides health tracking capabilities for monitoring daily health data.

* Blood glucose logs
* Food intake logs
* Historical health records

### AI Medical Assistant

GlucoSense includes an AI-powered chatbot designed to provide general health and diabetes-related information.

Capabilities include:

* Natural-language health questions
* Diabetes-related educational responses
* Health and nutrition guidance
* Conversation history
* Source-aware AI responses

The AI assistant is powered through the Groq API.

### Knowledge Center

Users can browse educational health articles and save useful resources for later.

* Article listing
* Article detail pages
* Article categories
* Saved articles
* Dynamic saved-resource statistics

### Doctor Recommendations

Users can browse healthcare professionals and find doctors based on their needs.

* Doctor directory
* Doctor details
* Specialist information
* Favorite doctors

### Authentication

The application provides token-based user authentication.

* User registration
* Login
* JWT authentication
* Protected API endpoints
* Logout
* Client-side token management

---

## Architecture

GlucoSense follows a frontend/backend-separated architecture.

```text
┌───────────────────────────────┐
│          GlucoSense           │
│        Web Application        │
└───────────────┬───────────────┘
                │
                │ HTTP / REST API
                ▼
┌───────────────────────────────┐
│          Django API           │
│           core_api            │
├───────────────────────────────┤
│ Authentication                │
│ Medical Profile               │
│ Assessment                    │
│ Health Tracking               │
│ Articles                      │
│ Doctors                       │
│ Favorites                     │
│ Chat History                  │
│ AI Chat                       │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│       PostgreSQL / Supabase   │
│           Database            │
└───────────────────────────────┘

                │
                ▼
┌───────────────────────────────┐
│       External AI Service     │
│             Groq              │
└───────────────────────────────┘
```

The frontend communicates with the Django backend through REST API endpoints. The backend handles authentication, business logic, database operations, and communication with the AI service.

---

## Tech Stack

### Backend

* Python
* Django
* REST API
* PostgreSQL
* Supabase
* JWT authentication

### Frontend

* HTML5
* CSS3
* JavaScript
* Django Templates
* Chart.js

### AI

* Groq API
* Large Language Model-based conversational assistant

### Development Tools

* Git
* GitHub
* Visual Studio Code

---

## Project Structure

```text
GlucoSense/
│
├── core/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── core_api/
│   ├── views.py
│   ├── urls.py
│   └── ...
│
├── accounts/
│   ├── views.py
│   ├── urls.py
│   └── ...
│
├── assessment/
│   ├── views.py
│   ├── urls.py
│   └── ...
│
├── chatbot/
│   ├── views.py
│   ├── urls.py
│   └── ...
│
├── dashboard/
├── doctors/
├── knowledge/
├── pages/
│
├── static/
│   ├── css/
│   └── js/
│
├── templates/
│   ├── accounts/
│   ├── chatbot/
│   ├── dashboard/
│   ├── doctors/
│   ├── knowledge/
│   └── ...
│
├── manage.py
├── requirements.txt
└── README.md
```

---

## API Overview

All core backend endpoints are exposed through the `/api/` prefix.

### Authentication

| Method | Endpoint         | Description         |
| ------ | ---------------- | ------------------- |
| POST   | `/api/register/` | Register a new user |
| POST   | `/api/login/`    | Authenticate a user |

### Medical Profile

| Method | Endpoint                | Description              |
| ------ | ----------------------- | ------------------------ |
| GET    | `/api/medical-profile/` | Retrieve medical profile |
| PUT    | `/api/medical-profile/` | Update medical profile   |

### Health Tracking

| Method | Endpoint             | Description           |
| ------ | -------------------- | --------------------- |
| GET    | `/api/glucose-logs/` | Retrieve glucose logs |
| POST   | `/api/glucose-logs/` | Create glucose log    |
| PUT    | `/api/glucose-logs/` | Update glucose log    |
| DELETE | `/api/glucose-logs/` | Delete glucose log    |
| GET    | `/api/food-logs/`    | Retrieve food logs    |
| POST   | `/api/food-logs/`    | Create food log       |
| PUT    | `/api/food-logs/`    | Update food log       |
| DELETE | `/api/food-logs/`    | Delete food log       |

### Assessment

| Method | Endpoint                   | Description                 |
| ------ | -------------------------- | --------------------------- |
| POST   | `/api/assessment/`         | Submit assessment           |
| GET    | `/api/assessment/history/` | Retrieve assessment history |
| GET    | `/api/assessment/<id>/`    | Retrieve assessment details |

### Knowledge Center

| Method | Endpoint                    | Description              |
| ------ | --------------------------- | ------------------------ |
| GET    | `/api/articles/`            | Retrieve articles        |
| GET    | `/api/articles/<id>/`       | Retrieve article details |
| GET    | `/api/saved-articles/`      | Retrieve saved articles  |
| POST   | `/api/saved-articles/`      | Save an article          |
| DELETE | `/api/saved-articles/<id>/` | Remove saved article     |

### Doctors

| Method | Endpoint                      | Description               |
| ------ | ----------------------------- | ------------------------- |
| GET    | `/api/doctors/`               | Retrieve doctors          |
| GET    | `/api/doctors/<id>/`          | Retrieve doctor details   |
| GET    | `/api/favorite-doctors/`      | Retrieve favorite doctors |
| POST   | `/api/favorite-doctors/`      | Add favorite doctor       |
| DELETE | `/api/favorite-doctors/<id>/` | Remove favorite doctor    |

### AI Chat

| Method | Endpoint             | Description                        |
| ------ | -------------------- | ---------------------------------- |
| POST   | `/api/chat/`         | Send a message to the AI assistant |
| GET    | `/api/chat-history/` | Retrieve chat history              |
| POST   | `/api/chat-history/` | Save chat history                  |

---

## Getting Started

### Prerequisites

Make sure the following software is installed:

* Python 3.10 or newer
* Git
* PostgreSQL or access to a Supabase PostgreSQL database

### Clone the Repository

```bash
git clone https://github.com/<your-username>/glucosense.git
cd glucosense
```

Replace `<your-username>` with the GitHub account that owns the repository.

### Create a Virtual Environment

For Windows:

```bash
python -m venv venv
```

Using Git Bash:

```bash
source venv/Scripts/activate
```

Using Command Prompt:

```cmd
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file in the project root.

```env
SECRET_KEY=your_django_secret_key
DEBUG=True

DATABASE_URL=your_database_url

GROQ_API_KEY=your_groq_api_key

JWT_SECRET_KEY=your_jwt_secret_key
```

Never commit `.env` or API keys to the repository.

Make sure `.env` is included in `.gitignore`.

### Apply Database Migrations

```bash
python manage.py migrate
```

### Run the Development Server

```bash
python manage.py runserver
```

The application will be available at:

```text
http://127.0.0.1:8000/
```

---

## Environment Variables

| Variable         | Description                           |
| ---------------- | ------------------------------------- |
| `SECRET_KEY`     | Django secret key                     |
| `DEBUG`          | Django debug mode                     |
| `DATABASE_URL`   | PostgreSQL database connection string |
| `GROQ_API_KEY`   | API key used for AI inference         |
| `JWT_SECRET_KEY` | Secret used for authentication tokens |

For production deployment, secrets should be configured through the hosting platform's environment variable management system.

---

## Deployment

GlucoSense is designed to be deployed using a cloud-based architecture.

A typical deployment configuration consists of:

```text
GitHub
   │
   ▼
Vercel
   │
   ├── Django Web Application
   │
   └── Static Assets
          │
          ▼
     External Services
     ├── Supabase PostgreSQL
     └── Groq API
```

Before deploying to production, ensure that:

* `DEBUG=False`
* `ALLOWED_HOSTS` is properly configured
* `CSRF_TRUSTED_ORIGINS` includes the production domain
* Environment variables are configured
* Static files are correctly configured
* Database connections are configured for production
* CORS and CSRF policies match the deployed domain
* API keys are not exposed to the frontend

---

## Security

GlucoSense handles user health-related information, making application security an important consideration.

Security considerations include:

* JWT authentication for protected API endpoints
* Password hashing through Django's authentication system
* Environment-based secret management
* Authorization headers for protected requests
* Server-side input validation
* User-specific database relationships

Sensitive credentials and API keys must never be committed to the repository.

---

## AI Disclaimer

GlucoSense uses artificial intelligence to provide general health-related information.

AI-generated responses:

* May contain inaccurate or incomplete information
* Should not be considered a medical diagnosis
* Should not replace professional medical consultation
* Should not be used as the sole basis for medical decisions
* Should not be relied upon during medical emergencies

Users should consult qualified healthcare professionals for medical diagnosis, treatment, or other important healthcare decisions.

---

## Project Status

**Status: Completed / Deployment Preparation**

The current implementation includes:

* User registration and authentication
* Medical profile management
* Health risk assessment
* Assessment history
* Risk trend visualization
* Health tracking APIs
* Educational articles
* Saved articles
* Doctor directory
* Favorite doctors
* AI chatbot
* Chat history
* Profile dashboard
* Dynamic health statistics
* Authentication pages

The project is currently being prepared for production deployment.

---

## Development

GlucoSense was developed as a collaborative software project with responsibilities divided across frontend development, backend development, AI integration, and system development.

The project uses Git-based version control with feature and integration branches before changes are merged into the main branch.

---

## License

This project is developed for educational and portfolio purposes.

A formal open-source license can be added if the project is intended to be publicly distributed or reused.

---

## Medical Disclaimer

GlucoSense is an educational and health-awareness platform.

It is not a medical device and does not provide professional medical diagnosis, treatment, or emergency medical services.

Always consult a qualified healthcare professional for medical decisions.
