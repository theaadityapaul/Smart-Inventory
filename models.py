# models.py
from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey, TIMESTAMP, Date
from sqlalchemy.orm import relationship
from database import Base

class Supplier(Base):
    __tablename__ = "suppliers"
    supplierid = Column(Integer, primary_key=True, index=True)
    suppliername = Column(String, nullable=False)
    email = Column(String, unique=True)
    
    Products = relationship("Product", back_populates="Supplier")

class Product(Base):
    __tablename__ = "products"
    productid = Column(Integer, primary_key=True, index=True)
    supplierid = Column(Integer, ForeignKey("suppliers.supplierid"))
    productname = Column(String, nullable=False)
    unitprice = Column(DECIMAL(10, 2), nullable=False, default=0.0)
    currentstock = Column(Integer, nullable=False, default=0)
    reorderlevel = Column(Integer, nullable=False, default=10)
    
    Supplier = relationship("Supplier", back_populates="Products")
    Sales = relationship("SalesTransaction", back_populates="Product")

class SalesTransaction(Base):
    __tablename__ = "salestransactions"
    saleid = Column(Integer, primary_key=True, index=True)
    productid = Column(Integer, ForeignKey("products.productid"))
    quantitysold = Column(Integer, nullable=False)
    saleprice = Column(DECIMAL(10, 2), nullable=False)
    saledate = Column(TIMESTAMP(timezone=True), server_default="NOW()")
    
    Product = relationship("Product", back_populates="Sales")

class DemandPrediction(Base):
    __tablename__ = "demandpredictions"
    predictionid = Column(Integer, primary_key=True, index=True)
    productid = Column(Integer, ForeignKey("products.productid"))
    predicteddemand = Column(Integer, nullable=False)
    predictionstartdate = Column(Date, nullable=False)
    predictionenddate = Column(Date, nullable=False)
    modelused = Column(String, nullable=False)