from fastapi import APIRouter, HTTPException
from app.models.schema import ChatRequest, ChatResponse
from app.services.agent import ask_data_whisperer

router = APIRouter()

# DÜZELTME: 'async def' yerine 'def' kullanıldı. 
# İçerideki ask_data_whisperer senkron (blocking) olduğu için, 
# 'def' kullanarak FastAPI'nin bunu threadpool'da çalıştırmasını sağlıyoruz.
@router.post("/query", response_model=ChatResponse)
def handle_chat_query(request: ChatRequest):
    """
    Frontend'den gelen doğrulanmış JSON isteğini alır, 
    Text-to-SQL ajanı ile işler ve sonucu döner.
    """
    try:
        result = ask_data_whisperer(request.question)
        
        # 1. Kontrollü Hatalar (Ajanın yakaladığı kural ihlalleri veya SQL hataları)
        if result.get("status") == "error":
            raise HTTPException(status_code=400, detail=result.get("message"))
            
        # 2. Başarılı Yanıt
        return ChatResponse(**result)
        
    except HTTPException:
        # 400 hatalarını ezmemek için tekrar yukarı fırlatıyoruz
        raise
    except Exception as e:
        # 3. Beklenmeyen Sistem Çökmeleri (Memory leak, API Timeout vb.)
        raise HTTPException(status_code=500, detail=f"Sunucu Hatası: {str(e)}")