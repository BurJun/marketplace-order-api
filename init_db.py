from sqlalchemy.orm import Session

from db import engine, SessionLocal
from models import Base, Product, CustomerOrder, OrderItem

def create_tables():
    Base.metadata.create_all(bind=engine)

def seed_data():
    db: Session = SessionLocal()
    try:
        if db.query(Product).first():
            print("Данные сущ")
            return
        product1 = Product(id=1, quantity=10, price=65000.00)
        product2 = Product(id=2, quantity=5, price=40000.00)

        db.add_all([product1,product2])

        order = CustomerOrder(id=1)
        db.add(order)
        db.flush()

        item1 = OrderItem(
            order_id = order.id,
            product_id = 1,
            quantity = 1,
            price = 65000.00,
        )

        db.add(item1)

        db.commit()
    except Exception as e:
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_tables()
    seed_data()