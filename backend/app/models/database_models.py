from sqlalchemy import Column, String, Integer, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base

class Customer(Base):
    __tablename__ = "customers"
    customer_id = Column(String(32), primary_key=True, index=True)
    customer_city = Column(String)
    customer_state = Column(String)
    
    # Bir müşterinin birden fazla siparişi olabilir
    orders = relationship("Order", back_populates="customer")

class Product(Base):
    __tablename__ = "products"
    product_id = Column(String(32), primary_key=True, index=True)
    product_category_name_english = Column(String)
    
    # Bir ürün birden fazla sipariş kaleminde yer alabilir
    order_items = relationship("OrderItem", back_populates="product")

class Order(Base):
    __tablename__ = "orders"
    order_id = Column(String(32), primary_key=True, index=True)
    customer_id = Column(String(32), ForeignKey("customers.customer_id"), index=True)
    order_status = Column(String)
    order_purchase_timestamp = Column(DateTime) 
    order_delivered_customer_date = Column(DateTime)
    
    # İlişkiler
    customer = relationship("Customer", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")
    payments = relationship("Payment", back_populates="order")
    reviews = relationship("Review", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"
    order_id = Column(String(32), ForeignKey("orders.order_id"), primary_key=True)
    # Yeni eklenen kolon, sipariş içindeki sırayı belirtir ve Primary Key'in parçasıdır
    order_item_id = Column(Integer, primary_key=True) 
    product_id = Column(String(32), ForeignKey("products.product_id"), index=True)
    price = Column(Numeric(10, 2))
    
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")

class Payment(Base):
    __tablename__ = "payments"
    order_id = Column(String(32), ForeignKey("orders.order_id"), primary_key=True)
    # Yeni eklenen kolon. Aynı order_id'ye sahip birden fazla ödeme olabilmesini sağlar.
    payment_sequential = Column(Integer, primary_key=True)
    payment_type = Column(String)
    payment_value = Column(Numeric(10, 2))
    
    order = relationship("Order", back_populates="payments")

class Review(Base):
    __tablename__ = "reviews"
    review_id = Column(String(32), primary_key=True)
    # order_id'yi de primary_key=True yapıyoruz
    order_id = Column(String(32), ForeignKey("orders.order_id"), primary_key=True, index=True)
    review_score = Column(Integer)
    
    order = relationship("Order", back_populates="reviews")