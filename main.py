# main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import pandas as pd
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta

from database import get_db, engine, Base
import models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Inventory API")

# --- CORRECT CORS FIX ---
origins = [
    "http://127.0.0.1:5501",  # Your Live Server port
    "http://localhost:5501"   # Your Live Server port
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --- END OF CORS FIX ---

@app.get("/")
def read_root():
    return {"message": "Welcome to the Smart Inventory Management System"}

@app.post("/products/add", status_code=201)
def add_product(name: str, stock: int, price: float, db: Session = Depends(get_db)):
    new_product = models.Product(
        productname=name,
        currentstock=stock,
        unitprice=price
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    
    # --- "ID UNDEFINED" FIX ---
    # Return a simple dictionary for JavaScript
    return {
        "productid": new_product.productid,
        "productname": new_product.productname,
        "currentstock": new_product.currentstock
    }

@app.post("/sales/record", status_code=201)
def record_sale(product_id: int, quantity: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.productid == product_id).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.currentstock < quantity:
        raise HTTPException(status_code=400, detail="Not enough stock")

    product.currentstock -= quantity
    
    new_sale = models.SalesTransaction(
        productid=product_id,
        quantitysold=quantity,
        saleprice=product.unitprice * quantity
    )
    db.add(new_sale)
    db.commit()
    db.refresh(product)
    
    return {"message": "Sale recorded", "product_name": product.productname, "new_stock": product.currentstock}

@app.post("/products/{product_id}/predict")
def predict_demand(product_id: int, db: Session = Depends(get_db)):
    
    query = f"""
        SELECT DATE_TRUNC('week', "saledate") AS week, SUM("quantitysold") AS total_sales
        FROM "salestransactions"
        WHERE "productid" = {product_id}
        GROUP BY week
        HAVING COUNT("saleid") > 0
        ORDER BY week;
    """
    df = pd.read_sql_query(query, con=engine)

    if len(df) < 4: 
        raise HTTPException(status_code=400, 
                            detail=f"Not enough sales data. Need at least 4 weeks. Found {len(df)}.")

    df = df.sort_values('week')
    df['time_index'] = range(1, len(df) + 1)
    X = df[['time_index']]
    y = df['total_sales']
    model = LinearRegression()
    model.fit(X, y)
    
    last_index = df['time_index'].max()
    future_indices = [[last_index + 1], [last_index + 2], [last_index + 3], [last_index + 4]]
    predicted_sales = model.predict(future_indices)
    total_future_demand = sum([max(0, int(p)) for p in predicted_sales])
    
    today = datetime.now().date()
    new_prediction = models.DemandPrediction(
        productid=product_id,
        predicteddemand=total_future_demand,
        predictionstartdate=today,
        predictionenddate=today + timedelta(weeks=4),
        modelused="LinearRegression"
    )
    db.add(new_prediction)
    db.commit()

    return {
        "message": "Prediction successful and saved.",
        "product_id": product_id,
        "predicted_demand_next_4_weeks": total_future_demand
    }