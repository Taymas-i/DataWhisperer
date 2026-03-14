from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.api.deps import get_db
from app.models.database_models import Customer, Product, Order, OrderItem, Payment, Review
from pydantic import BaseModel
from app.services.whisperer import ask_whisperer as groq_whisperer

router = APIRouter()

class UserQuery(BaseModel):
    question: str

@router.post("/ask", tags=["AI Whisperer"])
async def chat_with_db(query: UserQuery):
    """
    Main entry point for the LLM.
    Takes a natural language question and returns an AI-generated answer
    based on real-time data from your DB.
    """
    try:
        # Explicitly call the Groq version
        result = groq_whisperer(query.question)
        return {"answer": result}
    except Exception as e:
        # Log the full traceback for debugging
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail="The Whisperer is having trouble thinking..."
        )

# --- CUSTOMERS ---
@router.get("/customers/", tags=["Customers"])
def get_customers(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return db.query(Customer).offset(skip).limit(limit).all()

# --- PRODUCTS ---
@router.get("/products/", tags=["Products"])
def get_products(category: str = None, db: Session = Depends(get_db)):
    query = db.query(Product)
    if category:
        query = query.filter(Product.product_category_name_english == category)
    return query.limit(50).all()

# --- ORDERS (The Hub) ---
@router.get("/orders/{order_id}", tags=["Orders"])
def get_order_full_detail(order_id: str, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return {
        "order_info": order,
        "items": order.items,
        "payments": order.payments,
        "reviews": order.reviews
    }

# --- ANALYTICS / AGGREGATIONS ---
@router.get("/analytics/revenue-by-city", tags=["Analytics"])
def get_revenue_by_city(db: Session = Depends(get_db)):
    # Placeholder for future analytical queries (JOIN Customer, Order, OrderItem)
    pass