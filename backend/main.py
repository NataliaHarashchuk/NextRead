from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from database import engine, Base
import models

Base.metadata.create_all(bind=engine)
app= FastAPI()

@app.get('/')
def root():
    html_content='<h2>Hello World!</h2>'
    return HTMLResponse(content=html_content)