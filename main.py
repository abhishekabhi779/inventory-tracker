from fastapi import FastAPI, Depends, HTTPException, Query, Path, Body
from sqlalchemy.orm import Session
from pydantic import BaseModel
from models import Base, Product
from database import engine, get_db
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from fastapi.responses import StreamingResponse

app = FastAPI()
Base.metadata.create_all(bind=engine)

# Pydantic model for request/response validation
class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    stock: int

# CRUD Operations
@app.post("/products/")
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/products/{product_id}")
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.get("/products/")
async def get_products(
    name: str = Query(None, description="Filter by product name (partial match)"),
    min_stock: int = Query(None, description="Minimum stock level"),
    max_stock: int = Query(None, description="Maximum stock level"),
    db: Session = Depends(get_db)
):
    query = db.query(Product)
    if name:
        query = query.filter(Product.name.ilike(f"%{name}%"))  # Case-insensitive partial match
    if min_stock is not None:
        query = query.filter(Product.stock >= min_stock)
    if max_stock is not None:
        query = query.filter(Product.stock <= max_stock)
    return query.all()

@app.put("/products/{product_id}")
def update_product(product_id: int, product: ProductCreate, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in product.dict().items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted"}


class StockUpdate(BaseModel):
    quantity: int  # Amount to reduce stock by

@app.patch("/products/{product_id}/stock")
def update_stock(
    product_id: int, update: StockUpdate, db: Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.stock < update.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")
    product.stock -= update.quantity
    db.commit()
    db.refresh(product)
    return product    


@app.get("/analytics/")
def get_analytics(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    total_value = sum(product.price * product.stock for product in products)
    low_stock = [p for p in products if p.stock < 10]  # Threshold: 10
    return {
        "total_inventory_value": total_value,
        "low_stock_items": [
            {"id": p.id, "name": p.name, "stock": p.stock} for p in low_stock
        ]
    }

@app.get("/inventory-report/")
def generate_inventory_report(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    if not products:
        raise HTTPException(status_code=404, detail="No products found")

    # Create PDF in memory
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    data = [["ID", "Name", "Description", "Price", "Stock"]]  # Table header
    for product in products:
        data.append([product.id, product.name, product.description, product.price, product.stock])
    
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    doc.build([table])
    buffer.seek(0)
    return StreamingResponse(buffer, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=inventory_report.pdf"})