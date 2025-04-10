# URL Shortener Technical Documentation

## System Architecture

The URL shortener service is built using FastAPI and SQLAlchemy, following a modern microservices architecture pattern. The system consists of the following main components:

### Core Components

1. **FastAPI Application (app.py)**
   - Handles HTTP requests
   - Manages API endpoints
   - Implements request validation
   - Provides OpenAPI documentation

2. **Database Layer (db.py)**
   - Manages SQLAlchemy engine and session
   - Handles database connections
   - Provides session management utilities

3. **Data Models (models.py)**
   - Defines SQLAlchemy ORM models
   - Implements URL shortening logic
   - Handles data validation and persistence

## Database Integration

### Database Connection (db.py)

The database integration is handled through SQLAlchemy, providing a robust ORM layer:

```python
# Database connection configuration
DATABASE_URL = os.getenv('DATABASE_URL')  # Load from environment variables

# SQLAlchemy engine setup with connection pooling
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQLAlchemy models
Base = declarative_base()

# Database session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**Key Features:**
- Environment-based configuration
- Connection pooling for performance
- Automatic session cleanup
- FastAPI dependency injection ready

### Database Schema and Models

#### URL Model (models.py)

```python
class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, nullable=False)
    short_code = Column(String, unique=True, index=True, nullable=False)
```

**Model Methods:**
1. `generate_secure_short_code(length=8)`
   - Generates cryptographically secure random codes
   - Uses combination of letters and numbers
   - Configurable length parameter

2. `shorten_url(db: Session, original_url: str) -> str`
   - Handles URL shortening logic
   - Checks for existing URLs to prevent duplicates
   - Ensures unique short codes
   - Manages database transactions

3. `get_original_url(db: Session, short_code: str) -> str`
   - Retrieves original URL from short code
   - Returns None if not found

**Database Optimizations:**
- Indexed primary key for fast lookups
- Unique constraint on short_code
- Composite index on frequently queried columns

## FastAPI Implementation

### Request Validation

```python
from pydantic import BaseModel

class ShortenRequest(BaseModel):
    original_url: str  # Validates URL format
```

### API Endpoints

#### 1. Create Short URL

```python
@app.post("/shorten/")
def create_short_url(request: ShortenRequest, db: Session = Depends(get_db)):
    short_code = URL.shorten_url(db, request.original_url)
    return {"short_url": f"http://localhost:8000/{short_code}"}
```

**Features:**
- Automatic request validation via Pydantic
- Database session injection using FastAPI dependency system
- Structured JSON response

**Request Format:**
```json
{
    "url": "https://example.com/very/long/url"
}
```

**Response Format:**
```json
{
    "short_url": "http://domain.com/abc123"
}
```

#### 2. Redirect to Original URL

```python
@app.get("/{short_code}")
def redirect_to_url(short_code: str, db: Session = Depends(get_db)):
    url = URL.get_url_from_short_code(db, short_code)
    if url:
        return RedirectResponse(url=url.original_url)
    raise HTTPException(status_code=404, detail="URL not found")
```

**Features:**
- Path parameter validation
- Automatic 404 handling
- FastAPI RedirectResponse for proper HTTP redirects
- Database integration through dependency injection

**Response:** HTTP 302 Redirect to original URL

## Code Structure Deep Dive

### models.py Implementation

The `URL` class is the core model that handles URL shortening:

1. **Short Code Generation**
```python
@staticmethod
def generate_secure_short_code(length=8):
    """Generate a random alphanumeric short code"""
    characters = string.ascii_letters + string.digits
    return "".join(secrets.choice(characters) for _ in range(length))
```
This method generates secure random codes using Python's `secrets` module.

2. **URL Shortening Logic**
```python
@classmethod
def shorten_url(cls, db: Session, original_url: str) -> str:
    # Check for existing URL
    existing_url = db.query(cls).filter(cls.original_url == original_url).first()
    if existing_url:
        return existing_url.short_code

    # Generate unique short code
    short_code = cls.generate_secure_short_code()
    while db.query(cls).filter(cls.short_code == short_code).first():
        short_code = cls.generate_secure_short_code()

    # Create and save new URL
    new_url = cls(original_url=original_url, short_code=short_code)
    db.add(new_url)
    db.commit()

    return short_code
```

## URL Shortening Flow

1. Client submits original URL
2. System checks if URL exists in database
3. If exists, return existing short code
4. If not exists:
   - Generate random short code
   - Verify uniqueness
   - Store in database
   - Return new short code

## Redirection Mechanism

1. Client requests shortened URL
2. System looks up short code in database
3. If found, return 302 redirect to original URL
4. If not found, return 404 error

## Docker Deployment

### Container Structure

- Base Image: Python 3.9-slim
- Application Directory: /app
- Dependencies: requirements.txt
- Exposed Port: 8000

### Deployment Steps

1. Build Docker image:
```bash
docker build -t url-shortener .
```

2. Run container:
```bash
docker run -d -p 8000:8000 url-shortener
```

### Docker Compose Configuration

The service can be deployed using docker-compose:

```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: urlshortener
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
```

## Performance Considerations

1. **Database Indexing**
   - Short code index for fast lookups
   - Original URL index for duplicate checking

2. **Caching Strategy**
   - Implement Redis caching for frequently accessed URLs
   - Cache both forward and reverse lookups

3. **Load Balancing**
   - Horizontal scaling with multiple application instances
   - Database connection pooling

## Security Measures

1. **Short Code Generation**
   - Using cryptographically secure random generation
   - Avoiding predictable sequences

2. **Input Validation**
   - URL format validation
   - Length limits on original URLs
   - Character set restrictions on short codes

3. **Rate Limiting**
   - API endpoint rate limiting
   - IP-based request throttling