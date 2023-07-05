from fastapi import FastAPI
from database.db_setup import Base,engine
from app.routers import users

app = FastAPI()
Base.metadata.create_all(engine)


app.include_router(users.router)