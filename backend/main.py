from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from database import engine, Base, get_db
import models 

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get('/', response_class=HTMLResponse)
def root():
    html_content = '<h2>Hello World!</h2>'
    return html_content

@app.get('/items/')
def read_items(db: Session = Depends(get_db)):
    return {"message": "Database session is active"}