import os
import re
from dotenv import load_dotenv
from groq import Groq
from app.services.db_tools import get_database_schema, execute_sql_query

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("HATA: GROQ_API_KEY bulunamadı!")

client = Groq(api_key=GROQ_API_KEY)
# Karmaşık SQL yazımı için büyük model şart.
MODEL_NAME = "llama-3.3-70b-versatile" 

def generate_sql(user_question: str, schema: str) -> str:
    """
    Kullanıcı sorusunu ve DB şemasını alarak sadece SQL sorgusu döndürür.
    """
    system_prompt = f"""You are a Senior PostgreSQL Database Administrator.
Your ONLY purpose is to translate the user's natural language question into a highly optimized, correct PostgreSQL query.

CRITICAL RULES:
1. OUTPUT ONLY VALID SQL. DO NOT output any markdown formatting (like ```sql). DO NOT add explanations, greetings, or pleasantries.
2. You MUST use the exact table and column names provided in the schema below. Do not invent columns.
3. Use correct Primary Key and Foreign Key relationships for JOINs based on the schema.
4. Always apply 'LIMIT 100' to the end of the query unless the user explicitly asks for a smaller limit or an aggregate function (COUNT, MAX, SUM) makes it unnecessary. Protect the system from memory overload.
5. Only use SELECT statements (Read-Only).

DATABASE SCHEMA:
{schema}
"""
    
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_question}
        ],
        temperature=0.0, # Deterministic, sıfır yaratıcılık. Her zaman aynı SQL'i üretmeli.
        max_tokens=512
    )
    
    raw_sql = response.choices[0].message.content
    
    # Model inat edip markdown dönerse diye güvenlik temizliği (Regex)
    sql_match = re.search(r"```(?:sql)?\s*(.*?)\s*```", raw_sql, re.DOTALL | re.IGNORECASE)
    if sql_match:
        raw_sql = sql_match.group(1)
    
    return raw_sql.replace("```", "").strip()

def generate_human_response(user_question: str, sql_query: str, db_results: str) -> str:
    """
    Veritabanından dönen ham sonuçları kullanıcı dostu metne çevirir.
    """
    system_prompt = """You are an expert Data Analyst and E-Commerce Consultant.
Your job is to take raw database JSON/List results and translate them into a clear, professional, and concise natural language answer for an e-commerce executive.

RULES:
1. Answer the user's original question directly using ONLY the provided Data Results.
2. Do not mention the SQL query, database structure, or technical jargon in your answer. Act as if you just know the answer.
3. Keep the tone professional, minimalist, and business-focused.
4. If the Data Results are empty, politely state that no data was found for that specific criteria.
5. Provide the answer in Turkish (Türkçe).
"""

    user_payload = f"""
Original Question: {user_question}
SQL Used (For Context Only): {sql_query}
Data Results: {db_results}
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_payload}
        ],
        temperature=0.3, # Metin sentezleme için çok hafif bir yaratıcılık payı (daha doğal bir dil için)
        max_tokens=1024
    )
    
    return response.choices[0].message.content.strip()

def ask_data_whisperer(user_question: str) -> dict:
    """
    Ana Orkestratör Fonksiyon. FastAPI doğrudan bu fonksiyonu çağıracak.
    """
    try:
        # 1. Şemayı al
        schema = get_database_schema()
        
        # 2. SQL Üret
        sql_query = generate_sql(user_question, schema)
        
        # 3. SQL'i Çalıştır
        db_results = execute_sql_query(sql_query)
        
        # Eğer veritabanı hata döndürdüyse (örn: SECURITY_ERROR), bunu LLM'e geri besleyebilir
        # veya doğrudan kullanıcıya teknik hata olarak gösterebiliriz. Şimdilik logluyoruz.
        if isinstance(db_results, str) and ("ERROR" in db_results):
            return {"status": "error", "message": db_results}
            
        # 4. İnsani Yanıt Üret
        final_answer = generate_human_response(user_question, sql_query, str(db_results))
        
        return {
            "status": "success",
            "sql_used": sql_query,
            "data": db_results,
            "answer": final_answer
        }
        
    except Exception as e:
        return {"status": "error", "message": str(e)}