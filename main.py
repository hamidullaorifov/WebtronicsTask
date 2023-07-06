from fastapi import FastAPI
from database.db_setup import Base,engine
from app.routers import users,posts

app = FastAPI()
Base.metadata.create_all(engine)


app.include_router(users.router)
app.include_router(posts.router)