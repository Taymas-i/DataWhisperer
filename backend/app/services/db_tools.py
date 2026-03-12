from sqlalchemy import inspect, text
from sqlalchemy.exc import SQLAlchemyError
from typing import Union, List, Dict, Any
from app.database.session import engine

def get_database_schema() -> str:
    """
    LLM için veritabanı şemasını (Tablolar, Kolonlar, PK ve FK ilişkileri) 
    dinamik olarak okur ve metin formatında döndürür.
    """
    try:
        inspector = inspect(engine)
        schema_text = "Mevcut PostgreSQL Veritabanı Şeması:\n\n"
        
        for table_name in inspector.get_table_names():
            schema_text += f"Tablo: {table_name}\n"
            
            # Primary Key'leri bul
            pk_constraint = inspector.get_pk_constraint(table_name)
            pk_columns = pk_constraint.get('constrained_columns', [])
            
            # Kolonları ve Veri Tiplerini yaz
            for column in inspector.get_columns(table_name):
                col_name = column['name']
                col_type = str(column['type'])
                pk_marker = " [PRIMARY KEY]" if col_name in pk_columns else ""
                
                schema_text += f"  - {col_name} ({col_type}){pk_marker}\n"
            
            # Foreign Key'leri (İlişkileri) yaz - LLM'in JOIN yapabilmesi için kritik
            for fk in inspector.get_foreign_keys(table_name):
                constrained_col = fk['constrained_columns'][0]
                referred_table = fk['referred_table']
                referred_col = fk['referred_columns'][0]
                schema_text += f"  * İLİŞKİ: {constrained_col} -> {referred_table}.{referred_col}\n"
                
            schema_text += "\n"
            
        return schema_text.strip()
    
    except Exception as e:
        return f"Şema okunurken veritabanı hatası oluştu: {str(e)}"


def execute_sql_query(query: str) -> Union[List[Dict[str, Any]], str]:
    """
    LLM tarafından üretilen SQL sorgusunu güvenlik filtresinden geçirerek
    sadece okuma (Read-Only) modunda çalıştırır.
    """
    # 1. Güvenlik Kalkanı (Guardrail)
    clean_query = query.strip()
    
    # Sadece SELECT ve WITH (CTE) ile başlayan sorgulara izin veriyoruz
    if not clean_query.upper().startswith(("SELECT", "WITH")):
        return "SECURITY_ERROR: Sistem sadece okuma (Read-Only) yetkisine sahiptir. Yalnızca 'SELECT' veya 'WITH' ile başlayan sorgular kabul edilir. Lütfen sorguyu düzeltin."

    # 2. Güvenli Veritabanı Bağlantısı ve Çalıştırma
    try:
        with engine.connect() as connection:
            result = connection.execute(text(clean_query))
            rows = result.mappings().all()
            return [dict(row) for row in rows]
            
    except SQLAlchemyError as db_err:
        return f"EXECUTION_ERROR: SQL sorgusu veritabanında çalıştırılamadı. Hata: {str(db_err)}"
    except Exception as e:
        return f"SYSTEM_ERROR: Beklenmeyen bir hata oluştu: {str(e)}"