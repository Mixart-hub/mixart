from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Product

router = APIRouter(prefix="/admin")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def admin_panel(db: Session = Depends(get_db)):
    return db.query(Product).all()

@router.post("/add")
def add_product(
    name: str = Form(...),
    price: float = Form(...),
    quantity: int = Form(...),
    db: Session = Depends(get_db)
):
    product = Product(name=name, price=price, quantity=quantity)
    db.add(product)
    db.commit()
    return {"status": "added"}
