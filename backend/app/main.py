from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.database.session import engine, Base
from app.api import routes, auth
from app.services.whisperer import ask_whisperer

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="DataWhisperer API")

# Configure CORS
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include existing API routes
app.include_router(routes.router)
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])


@app.get("/")
def read_root():
    return {"message": "Welcome to DataWhisperer API"}


class QuestionRequest(BaseModel):
    question: str


@app.post("/ask")
async def ask_ai(payload: QuestionRequest):
    try:
        answer = ask_whisperer(payload.question)
        return {"answer": answer}
    except Exception as e:
        return {"error": str(e)}