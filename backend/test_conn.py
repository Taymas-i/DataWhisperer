from app.database.session import SessionLocal
from sqlalchemy import text

def test_connection():
    db = SessionLocal()
    try:
        # Simple SQL check
        result = db.execute(text("SELECT current_database();"))
        db_name = result.scalar()
        print(f"🚀 Successfully connected to Neon! Database: {db_name}")
        
        # Check if a table exists and has data
        customer_count = db.execute(text("SELECT COUNT(*) FROM customers")).scalar()
        print(f"📊 Current Customer Count: {customer_count}")
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_connection()