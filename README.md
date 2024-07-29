# CRB Inventory REST API

## How to run project

### Requirements

- Python 3.12
- Poetry

### Environment

Create a `.env` file in the root of the project with the content of .env.example and fill the variables with the correct values.

### Install dependencies

```bash
poetry install
```

### Local database setup using docker-compose

- Requires Docker and Docker Compose installed
- Requires the `.env` file to be created

```bash
poetry run task local-env-up
```

### Run migrations

```bash
poetry run task migrate
```

### Run project in development mode

```bash
poetry run task dev
```
### API Documentation

After running the project, you can access the API documentation at `http://localhost:8000/v1/docs`

### Run tests

```bash
poetry run task test
```

### Additional commands

```bash
poetry run task -l
```
