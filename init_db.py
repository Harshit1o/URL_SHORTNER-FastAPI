from db import Base, engine
import models  # This imports the models so they are registered with Base.metadata


def init_db():
    """Initialize the database by creating all tables."""
    # Create tables in the database
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")


if __name__ == "__main__":
    init_db()