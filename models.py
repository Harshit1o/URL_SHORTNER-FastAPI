from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from db import Base
import secrets
import string


class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, nullable=False)
    short_code = Column(String, unique=True, index=True, nullable=False)
    @staticmethod
    def generate_secure_short_code(length=8):
        """Generate a random alphanumeric short code generation"""
        characters = string.ascii_letters + string.digits  # a-z, A-Z, 0-9
        return "".join(secrets.choice(characters) for _ in range(length))

    @classmethod
    def shorten_url(cls, db: Session, original_url: str) -> str:
        """Shorten the given original URL."""
        existing_url = db.query(cls).filter(cls.original_url == original_url).first()
        if existing_url:
            return existing_url.short_code

        short_code = cls.generate_secure_short_code()

        while db.query(cls).filter(cls.short_code == short_code).first():
            short_code = cls.generate_secure_short_code()

        new_url = cls(original_url=original_url, short_code=short_code)
        db.add(new_url)
        db.commit()

        return short_code

    @classmethod
    def get_original_url(cls, db: Session, short_code: str) -> str:
        """Retrieve the original URL for the given short code."""
        url_entry = db.query(cls).filter(cls.short_code == short_code).first()
        if url_entry:
            return url_entry.original_url
        return None

    @classmethod
    def get_url_from_short_code(cls, db: Session, short_code: str) -> "URL":
        """Retrieve the URL object based on the short code."""
        url = db.query(cls).filter(cls.short_code == short_code).first()
        if url:
            return url
        return None