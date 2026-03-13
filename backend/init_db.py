from app.database.session import engine, Base
from app.models.database_models import Customer, Product, Order, OrderItem, Payment, Review 

def create_tables():
    print("Neon PostgreSQL üzerinde tablolar oluşturuluyor...")
    try:
        Base.metadata.create_all(bind=engine)
        print("İşlem başarıyla tamamlandı. Tablolar hazır.")
    except Exception as e:
        print(f"Hata oluştu: {e}")

if __name__ == "__main__":
    create_tables()