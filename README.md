# Django_Docker

How to run Django with Docker

### Publish app image to Docker Hub
docker login
docker build -t jasminlb/library-app:latest .
docker push jasminlb/library-app:latest

### PostgreSQL database settings
cp .env.example .env

### Run with Docker Compose
docker compose pull
docker compose up --build

Library application will be available at `http://localhost:8000`.

### Stop containers
docker compose down
