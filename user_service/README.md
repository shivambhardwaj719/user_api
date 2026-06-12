# User Service

Welcome to the **User Service**, a modern, production-ready backend built with **FastAPI**. This service is responsible for managing users, staff, authentication, and hospital-agnostic operations.

## Architecture & Features

This service employs a robust **Repository-Service Pattern** separating business logic from database interactions and API routing.

### Core Features
- **User & Staff Management**: CRUD endpoints with decoupled database interactions.
- **Centralized Handlers**: Standardized error handling, HTTP responses, and message constants.
- **Custom Middlewares**:
  - `JWTAuthenticationMiddleware`: Intercepts requests, validates tokens, and injects user context.
  - `GlobalRateLimitMiddleware`: Thread-safe rate limiting using an in-memory sliding window cache.
  - `APILoggerMiddleware`: Intercepts and logs all request/response cycles.
- **Real-Time Push Notifications**: Firebase Cloud Messaging (FCM) integration built to alert super admins automatically upon successful user/staff creations.
- **Background Scheduler**: Integrated `APScheduler` configured to compile and log the total active user count automatically at 23:59 everyday.
- **DevOps Ready**: Pre-configured with a `Dockerfile`, `docker-compose.yml`, and Kubernetes deployment manifests.

## Setup Instructions

### Local Development

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Firebase (Optional but Recommended)**:
   Place your Firebase Admin SDK service account key at the root of the project as `firebase-credentials.json`, or set the `FIREBASE_CREDENTIALS_PATH` environment variable. If omitted, the system gracefully defaults to mocking notification logs.

3. **Run the Application**:
   ```bash
   uvicorn app.main:app --reload
   ```

### Docker

You can easily spin up the application utilizing Docker Compose:

```bash
docker compose up --build
```
This automatically builds the optimized python slim image and exposes the FastAPI service on `http://localhost:8000`.

### Kubernetes

To deploy the user service into a Kubernetes cluster, utilize the provided manifests:

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```
*Note: Ensure your load balancer and ingress controllers are configured to expose the ClusterIP service properly.*

## Project Structure

```text
user_service/
├── app/
│   ├── api/          # API Routers and Endpoints (v1, deps)
│   ├── core/         # Core application setup (APScheduler)
│   ├── middleware/   # Custom FastAPI HTTP Middlewares
│   ├── models/       # SQLAlchemy ORM Models
│   ├── repositories/ # Database query abstraction layer
│   ├── schemas/      # Pydantic validation models
│   ├── services/     # Business logic layer
│   └── utils/        # Shared utilities (pagination, validation, notifications)
├── k8s/              # Kubernetes Deployment & Service Manifests
├── Dockerfile        # Docker Image Definition
├── docker-compose.yml# Docker Compose Definition
├── requirements.txt  # Python Dependencies
└── .gitignore        # Git Ignored Files
```
