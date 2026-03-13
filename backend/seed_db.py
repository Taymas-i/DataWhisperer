import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from sqlalchemy import text

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("HATA: .env dosyasında DATABASE_URL bulunamadı!")

engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    try:
        # Customers tablosunda veri var mı diye bakıyoruz
        result = conn.execute(text("SELECT COUNT(*) FROM customers")).scalar()
        if result > 0:
            print("🛑 DİKKAT: Veritabanında zaten veri var! Mükerrer (çift) kayıt oluşmasını engellemek için işlem iptal edildi.")
            print("Eğer veritabanını sıfırlamak istiyorsanız önce tabloları manuel olarak DROP etmelisiniz.")
            exit() 
    except Exception:
        
        pass

csv_files_ordered = [
    ('customers', 'backend/csv/cleaned_csv/customers.csv'),
    ('products', 'backend/csv/cleaned_csv/products.csv'),
    ('orders', 'backend/csv/cleaned_csv/orders.csv'),
    ('order_items', 'backend/csv/cleaned_csv/order_items.csv'),
    ('payments', 'backend/csv/cleaned_csv/payments.csv'),
    ('reviews', 'backend/csv/cleaned_csv/reviews.csv') 
]

print("Veriler Neon'a aktarılıyor. Mimari kurallara (Foreign Keys) uyuluyor...\n")

for table_name, file_path in csv_files_ordered:
    if os.path.exists(file_path):
        print(f"⏳ {table_name} okunuyor...")
        df = pd.read_csv(file_path)
        
        if table_name == 'orders':
            df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
            df['order_delivered_customer_date'] = pd.to_datetime(df['order_delivered_customer_date'])

        try:
            df.to_sql(table_name, engine, if_exists='append', index=False)
            print(f"✅ {table_name} başarıyla eklendi!")
        except Exception as e:
            print(f"❌ {table_name} yüklenirken HATA: {e}")
            break 
    else:
        print(f"❌ DOSYA BULUNAMADI: {file_path}")

print("\nVeritabanı besleme işlemi (Seeding) tamamlandı.")