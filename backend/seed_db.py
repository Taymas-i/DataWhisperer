import csv
import os
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.models.database_models import Customer, Product, Order, OrderItem, Payment

# Define the base folder path
BASE_CSV_PATH = "csv/cleaned_csv"

def seed_file(file_name, model_class):
    db: Session = SessionLocal()
    # Combining the folder path and the file name
    file_path = os.path.join(BASE_CSV_PATH, file_name)

    if not os.path.exists(file_path):
        print(f"⚠️ Skipping: {file_name} not found at {file_path}")
        return

    print(f"⌛ Seeding {file_name}...")
    
    try:
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # This creates an object of the class (Customer, Product, etc.)
                # using the data from the CSV row
                obj = model_class(**row) 
                db.add(obj)
            db.commit()
            print(f"✅ {file_name} completed.")
    except Exception as e:
        print(f"❌ Error in {file_name}: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    # IMPORTANT: We seed them in order because of Foreign Key dependencies
    seed_file("customers.csv", Customer)
    seed_file("products.csv", Product)
    seed_file("orders.csv", Order)
    seed_file("order_items.csv", OrderItem)
    seed_file("payments.csv", Payment)