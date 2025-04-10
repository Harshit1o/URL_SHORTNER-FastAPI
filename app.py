from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from db import get_db
from models import URL

app = FastAPI()


from pydantic import BaseModel

class ShortenRequest(BaseModel):
    original_url: str

@app.post("/shorten/")
def create_short_url(request: ShortenRequest, db: Session = Depends(get_db)):
    short_code = URL.shorten_url(db, request.original_url)
    return {"short_url": f"http://localhost:8000/{short_code}"}


@app.get("/{short_code}")
def redirect_to_url(short_code: str, db: Session = Depends(get_db)):
    url = URL.get_url_from_short_code(db, short_code)
    if url:
        return RedirectResponse(url=url.original_url)
    raise HTTPException(status_code=404, detail="URL not found")
