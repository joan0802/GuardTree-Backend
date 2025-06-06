# GuardTree API

A FastAPI-based backend using Supabase as the database.

## Setup

1. Clone the repository
2. Create a `.env` file in the root directory with the following variables:
   ```
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_service_role_key
   JWT_SECRET_KEY=your_secret_key
   GEMINI_API_KEY=your_LLM_api_key
   ```
   
   > **Important**: The application requires these environment variables to connect to Supabase. Make sure to create the `.env` file before starting the Docker container.

## Running with Docker

### Prerequisites
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Start the application
```bash
# Build the Docker image
docker compose build

# Start the containers
docker compose up -d
```

The API will be available at http://localhost:8000

### View logs
```bash
docker compose logs -f
```

### Stop the application
```bash
docker compose down
```

## API Documentation

FastAPI automatically generates documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Running Tests

The project uses pytest for testing. To run the tests, execute:

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/api/test_users.py

# Run specific test function
pytest tests/api/test_users.py::test_get_all_users
```

When running tests within Docker:

```bash
docker compose exec api pytest
```

## Project Structure

```
app/
├── core/
│   ├── auth.py             # Authentication utilities
│   └── supabase_client.py  # Supabase client
├── controllers/
│   ├── auth_controller.py  # Authentication endpoints
│   └── user_controller.py  # User endpoints
├── models/
│   └── user.py             # User data models
├── repositories/
│   └── user_repository.py  # Database interactions
├── services/
│   └── user_service.py     # Business logic
└── main.py                 # Main application file

tests/
├── api/                    # API endpoint tests
│   ├── test_auth.py        # Authentication endpoint tests
│   └── test_users.py       # User endpoint tests
└── unit/                   # Unit tests
    ├── test_user_repository.py  # Repository tests
    └── test_user_service.py     # Service tests
```

## Troubleshooting

### Supabase connection error
If you see an error like `supabase._sync.client.SupabaseException: supabase_key is required`, make sure your `.env` file is properly configured with the correct Supabase URL and key.

Also, ensure the `.env` file is not included in the `.dockerignore` file. If it is, update the .dockerignore file to allow the .env file to be copied into the container.
