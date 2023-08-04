from sqlalchemy import BigInteger, Column, Integer, String

from src.db.database import Base


class ProductBase(Base):
    article = Column(BigInteger, unique=True, nullable=False)
    product_type = Column(String, default=None)
    manufacturer = Column(String, default=None)
    product_name = Column(String, default=None)
    product_price = Column(Integer, default=0)
    in_stock = Column(Integer, default=0)
    product_model = Column(String, default=None)
    product_image = Column(String, default=None)


class FirstStore(ProductBase):
    __tablename__ = "first_store"


class SecondStore(ProductBase):
    __tablename__ = "second_store"


class ThirdStore(ProductBase):
    __tablename__ = "third_store"
