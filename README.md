# NXOC Backend

Django REST API with Django REST Framework, JWT authentication, CORS support, and Docker development tooling.

## Run locally

```bash
./env/bin/python manage.py migrate
./env/bin/python manage.py runserver
```

## Run with Docker

```bash
docker compose up --build
```

JWT endpoints use the configured API version (default `v1`):

- `POST /api/v1/token/`
- `POST /api/v1/token/refresh/`
