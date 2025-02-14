from sqlalchemy.orm import Session
from models import Supplier, Product

def chatbot_response(query: str, db: Session):
    """Handles chatbot query and returns a response."""

    if "supplier" in query.lower():
        suppliers = db.query(Supplier).all()
        return [supplier.name for supplier in suppliers]
    
    elif "product" in query.lower():
        products = db.query(Product).all()
        return [product.name for product in products]
    
    return "I can provide information about suppliers and products."
