from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch
from models import Product, Supplier
from database import SessionLocal
from fastapi.middleware.cors import CORSMiddleware

# Use a smaller, efficient model
MODEL_PATH = "distilgpt2"

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForCausalLM.from_pretrained(MODEL_PATH)

# Hugging Face pipeline for text generation
generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

app = FastAPI()

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Chatbot API!"}

# Generate AI response
def get_ai_response(query: str, data: str):
    prompt = f"""
    Below is the requested information for: {query}.

    Data:
    {data}

    Question: {query}
    """
    response = generator(prompt, max_length=200, num_return_sequences=1)
    return response[0]['generated_text'].strip()

@app.get("/query")
def handle_query(query: str, db: Session = Depends(get_db)):
    query_lower = query.lower().strip()
    
    try:
        # Fetch all products
        if "products" in query_lower:
            category = query_lower.replace("products", "").strip()
            products = db.query(Product).filter(Product.category.ilike(f"%{category}%")).all() if category else db.query(Product).all()
            
            if not products:
                return {"response": f"No products found in category '{category}'."} if category else {"response": "No products found."}
            
            data = "\n".join([f"{p.name} - {p.category}, Price: ${p.price}" for p in products])
            return {"response": get_ai_response(query, data)}
        
        # Fetch all suppliers
        elif "suppliers" in query_lower:
            suppliers = db.query(Supplier).all()
            if not suppliers:
                return {"response": "No suppliers found."}
            data = "\n".join([f"{s.name} - Contact: {s.contact_info}" for s in suppliers])
            return {"response": get_ai_response(query, data)}

        # Fetch product/supplier by name
        elif "name" in query_lower:
            name_query = query.split()[-1]
            products = db.query(Product).filter(Product.name.ilike(f"%{name_query}%")).all()
            suppliers = db.query(Supplier).filter(Supplier.name.ilike(f"%{name_query}%")).all()

            if not products and not suppliers:
                return {"response": f"No product or supplier found matching '{name_query}'."}
            
            product_data = "\n".join([f"Product: {p.name} - {p.category}, Price: ${p.price}" for p in products])
            supplier_data = "\n".join([f"Supplier: {s.name} - Contact: {s.contact_info}" for s in suppliers])
            
            data = f"{product_data}\n{supplier_data}".strip()
            return {"response": get_ai_response(query, data)}
        
        # Fetch by ID
        elif "id" in query_lower:
            id_value = ''.join(filter(str.isdigit, query))
            if id_value:
                id_value = int(id_value)
                product = db.query(Product).filter(Product.id == id_value).first()
                supplier = db.query(Supplier).filter(Supplier.id == id_value).first()
                
                if product:
                    data = f"{product.name} - {product.category}, Price: ${product.price}, Description: {product.description}"
                    return {"response": get_ai_response(f"Details for product ID {id_value}", data)}
                elif supplier:
                    data = f"{supplier.name} - Contact: {supplier.contact_info}"
                    return {"response": get_ai_response(f"Details for supplier ID {id_value}", data)}
                else:
                    return {"response": f"No product or supplier found with ID {id_value}."}
            return {"response": "Invalid query format for ID search."}
        
        return {"response": "Invalid query. Please ask about products, suppliers, categories, or IDs."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Fetch all products
@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    if not products:
        raise HTTPException(status_code=404, detail="No products found")
    data = "\n".join([f"{p.name} - {p.category}, Price: ${p.price}" for p in products])
    return {"response": get_ai_response("List all products", data)}

# Fetch product by ID
@app.get("/products/{product_id}")
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    data = f"{product.name} - {product.category}, Price: ${product.price}, Description: {product.description}"
    return {"response": get_ai_response(f"Details for product ID {product_id}", data)}

# Fetch all suppliers
@app.get("/suppliers")
def get_suppliers(db: Session = Depends(get_db)):
    suppliers = db.query(Supplier).all()
    if not suppliers:
        raise HTTPException(status_code=404, detail="No suppliers found")
    data = "\n".join([f"{s.name} - Contact: {s.contact_info}" for s in suppliers])
    return {"response": get_ai_response("List all suppliers", data)}

# Fetch supplier by ID
@app.get("/suppliers/{supplier_id}")
def get_supplier_by_id(supplier_id: int, db: Session = Depends(get_db)):
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    data = f"{supplier.name} - Contact: {supplier.contact_info}"
    return {"response": get_ai_response(f"Details for supplier ID {supplier_id}", data)}
