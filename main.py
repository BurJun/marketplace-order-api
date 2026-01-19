from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from db import get_session, engine
from models import Base, Product, CustomerOrder, OrderItem
from schemas import AddItemRequest, OrderItemResponse

app = FastAPI(title = "Order service")

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

@app.post("/orders/items", response_model = OrderItemResponse)
def add_item_to_order(body: AddItemRequest, db: Session = Depends(get_session)):
    order = db.get(CustomerOrder, body.order_id)
    if not order:
        raise HTTPException(status_code=404, detail= "Order not found")
    
    product =db.get(Product, body.product_id)
    if not product:
        raise HTTPException(status_code = 404, detail = "Product not found")
    
    if product.quantity < body.quantity:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "Not enough stock for this product"
        )
    
    stmt = (
        select(OrderItem)
        .where(
            OrderItem.order_id == body.order_id,
            OrderItem.product_id == body.product_id
        )
        .with_for_update()
    )
    existing_item = db.scalars(stmt).first()

    if existing_item:
        existing_item.quantity += body.quantity
        order_item = existing_item
    else:
        order_item = OrderItem(
            order_id = body.order_id,
            product_id = body.product_id,
            quantity = body.quantity,
            price = product.price,
        )
        db.add(order_item)

    product.quantity -= body.quantity

    db.commit()
    db.refresh(order_item)

    return OrderItemResponse(
        order_id = order_item.order_id,
        product_id = order_item.product_id,
        quantity = order_item.quantity,
    )
