# Phonebook Application

A MongoDB-based phonebook application with REST API endpoints, built with Django and Python.

## Features

- CRUD operations for contacts
- MongoDB integration using Djongo
- Docker support
- CI/CD pipeline with GitHub Actions
- Unit tests

## Prerequisites

- Python 3.9+
- MongoDB
- Docker and Docker Compose (for containerized deployment)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd phonebook
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file with the following content:
```
MONGODB_URI=mongodb://localhost:27017/
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=True
```

4. Run migrations:
```bash
python manage.py migrate
```

## Running the Application

### Local Development

1. Start MongoDB:
```bash
mongod
```

2. Run the application:
```bash
python manage.py runserver
```

### Using Docker

1. Build and run using Docker Compose:
```bash
docker-compose up --build
```

## API Endpoints

- `GET /api/contacts/` - Get all contacts
- `POST /api/contacts/` - Add a new contact
- `GET /api/contacts/<name>/` - Get a specific contact
- `PUT /api/contacts/<name>/` - Update a contact
- `DELETE /api/contacts/<name>/` - Delete a contact

## Running Tests

```bash
pytest
```

## CI/CD Pipeline

The application includes a GitHub Actions workflow that:
1. Runs tests on every push and pull request
2. Builds and pushes Docker image to DockerHub on main branch

To set up the CI/CD pipeline:
1. Add the following secrets to your GitHub repository:
   - `DOCKERHUB_USERNAME`
   - `DOCKERHUB_TOKEN`

## License

MIT 