from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base  # ✅ Import Base from database.py

# ✅ Define Supplier Model
class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    contact_info = Column(String(255), nullable=False)

    # Relationship with Product
    products = relationship("Product", back_populates="supplier", cascade="all, delete")

# ✅ Define Product Model
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    category = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)  # ✅ Corrected price type
    description = Column(String(255), nullable=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id", ondelete="CASCADE"), nullable=False)

    # Relationship with Supplier
    supplier = relationship("Supplier", back_populates="products")
