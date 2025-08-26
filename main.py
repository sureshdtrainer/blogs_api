from fastapi import FastAPI
from db.database import create_db_and_tables
from routers import blogs

app = FastAPI()

app.include_router(blogs.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
