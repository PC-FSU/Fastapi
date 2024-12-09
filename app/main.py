from fastapi import FastAPI
from . import ORM_models
from .database import engine
from .routers import posts, users

# Create all tables in the database
ORM_models.Base.metadata.create_all(engine)

app = FastAPI()
app.include_router(posts.router)
app.include_router(users.router)

@app.get('/')
async def root():
    return {"message": "Welcome to my api"}
