from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.chat import router as chat_router

app = FastAPI(
    title="DataWhisperer API",
    description="E-ticaret verileri için Text-to-SQL otonom ajanı.",
    version="1.0.0"
)

# CORS Ayarları - Arkadaşının React (localhost:3000 veya Vite: 5173) uygulamasının 
# API'a erişebilmesi için güvenlik kalkanını esnetiyoruz.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Canlıda (Production) buraya sadece Frontend'in net domaini yazılır.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Yazdığımız API rotasını uygulamaya monte ediyoruz
app.include_router(chat_router, prefix="/api/v1/agent", tags=["AI Agent"])

@app.get("/")
def health_check():
    return {"status": "healthy", "message": "DataWhisperer API sistemleri aktif."}