from pydantic import BaseModel, Field
from typing import Optional, Union, List, Dict, Any

class ChatRequest(BaseModel):
    # En az 3 karakter olmalı, boş istekleri (whitespace) engeller. Maksimum 500 karakter.
    question: str = Field(..., min_length=3, max_length=500, description="Kullanıcının doğal dilde sorduğu veri sorusu.")

class ChatResponse(BaseModel):
    status: str
    sql_used: Optional[str] = None
    data: Optional[Union[List[Dict[str, Any]], str]] = None
    answer: Optional[str] = None
    message: Optional[str] = None