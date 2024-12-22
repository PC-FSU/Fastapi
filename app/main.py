from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import ORM_models
from .database import engine
from .routers import posts, users, auth, vote
from .config import settings

# Create all tables in the database
# ORM_models.Base.metadata.create_all(engine)  # We don't need to this line as we are using alembic

app = FastAPI()

origins = ["*"] # list of domain that can talk to our api.

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get('/')
async def root():
    return {"message": "Welcome to my api!!!"}
