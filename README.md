# URL Shortener Service

A modern URL shortening service built with FastAPI, PostgreSQL, and Docker. This service allows you to create shortened versions of long URLs, making them easier to share and manage.

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs with Python
- **PostgreSQL**: Robust, open-source relational database
- **Docker**: Containerization platform for easy deployment
- **SQLAlchemy**: SQL toolkit and ORM for Python
- **Uvicorn**: Lightning-fast ASGI server implementation

## Project Structure

```
├── app.py           # Main FastAPI application
├── db.py            # Database connection and session management
├── models.py        # SQLAlchemy models
├── init_db.py       # Database initialization script
├── requirements.txt # Python dependencies
├── Dockerfile       # Docker container configuration
└── docker-compose.yml # Docker services configuration
```

## Getting Started

### Prerequisites

- Docker and Docker Compose installed on your system
- Python 3.9 or higher (for local development)

### Installation and Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. Configure environment variables:
   - Open `docker-compose.yml` and update the following values:
     ```yaml
     POSTGRES_PASSWORD: your_password
     POSTGRES_DB: url_shortener_db
     DATABASE_URL: postgresql://postgres:your_password@db:5432/url_shortener_db
     ```

3. Build and start the containers:
   ```bash
   docker-compose up --build
   ```

4. Initialize the database:
   ```bash
   docker-compose exec web python init_db.py
   ```

The service will be available at `http://localhost:8000`

### Local Development Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up PostgreSQL locally and update the database URL in the code

4. Run the application:
   ```bash
   uvicorn app:app --reload
   ```

## API Usage

### Shorten URL
- **Endpoint**: `POST /shorten/`
- **Request Body**:
  ```json
  {
    "original_url": "https://example.com/very/long/url/that/needs/shortening"
  }
  ```
- **Response**:
  ```json
  {
    "short_url": "http://localhost:8000/abc123"
  }
  ```

### Access Shortened URL
- Simply visit the shortened URL in your browser
- Example: `http://localhost:8000/abc123`
- You will be redirected to the original URL

## Docker Configuration

### Services

1. **Database (db)**:
   - PostgreSQL 13 Alpine
   - Exposed on port 5432
   - Persistent volume for data storage

2. **Web Application (web)**:
   - Python 3.9 slim image
   - FastAPI application
   - Hot-reload enabled for development
   - Exposed on port 8000

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.