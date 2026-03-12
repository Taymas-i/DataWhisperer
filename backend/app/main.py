from fastapi import FastAPI
from app.database.session import engine, Base
from app.api import routes

# This line creates the actual tables in your database file automatically
Base.metadata.create_all(bind=engine)

app = FastAPI(title="DataWhisperer API")

# We "include" the routes we defined in the api folder
app.include_router(routes.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to DataWhisperer!"}