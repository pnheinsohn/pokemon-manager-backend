
## Quick Start with Docker

1. Clone the repository:
```bash
git clone <repository-url>
cd django-tutorial/backend
```

2. Create a `.env` file in the `src` directory with your environment variables:
```bash
cp src/.env.example src/.env  # Adjust variables as needed
```

3. Start the services:
```bash
docker compose up -d
```

This will start:
- Django server at http://localhost:8000
- RabbitMQ management at http://localhost:15672
- Flower (Celery monitoring) at http://localhost:5555

## Services

- **backend**: Django web server
- **celery_worker**: Task queue worker
- **rabbitmq**: Message broker
- **flower**: Celery task monitoring

## Development

### Using Docker (Recommended)

The project is configured to support hot-reload in development:

```bash
docker compose up
```

### Local Development with Poetry

1. Install dependencies:
```bash
poetry install
```

2. Activate the virtual environment:
```bash
poetry shell
```

3. Run migrations:
```bash
cd src
python manage.py migrate
```

4. Start the development server:
```bash
python manage.py runserver
```

## Monitoring

- **RabbitMQ Dashboard**: http://localhost:15672
  - Default credentials: guest/guest
- **Flower Dashboard**: http://localhost:5555

## Data Persistence

- Django data is persisted in the `django_data` Docker volume
- Source code changes in the `src` directory are immediately reflected in the running containers, except for tasks... you have to rerun workers for that

## Contributing

1. Create a feature branch
2. Make your changes
3. Submit a pull request

## Notes

- The `.env` file is git-ignored for security
- Data in `src/data/` is git-ignored
- Python cache files and virtual environments are excluded from Docker builds
