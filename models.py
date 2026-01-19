from sqlalchemy import Column, Integer, BigInteger, ForeignKey, Numeric
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Product(Base):
    __tablename__ = "product"
    id = Column(BigInteger, primary_key=True)
    quantity = Column(Integer, nullable = False)
    price = Column(Numeric(10,2), nullable = False)

class CustomerOrder(Base):
    __tablename__ = "customer_order"
    id = Column(BigInteger, primary_key = True)

class OrderItem(Base):
    __tablename__ = "order_item"
    id = Column(BigInteger, primary_key = True)
    order_id = Column(BigInteger, ForeignKey("customer_order.id"), nullable = False)
    product_id = Column(BigInteger, ForeignKey("product.id"), nullable = False)
    quantity = Column(Integer, nullable = False)
    price = Column(Numeric(10, 2), nullable = False)
    order = relationship("CustomerOrder", backref ="items")
    product = relationship("Product")