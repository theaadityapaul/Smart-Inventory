-- schema.sql
DROP TABLE IF EXISTS demandpredictions, reorderhistory, salestransactions, products, suppliers CASCADE;

CREATE TABLE suppliers (
    supplierid SERIAL PRIMARY KEY,
    suppliername VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE
);

CREATE TABLE products (
    productid SERIAL PRIMARY KEY,
    supplierid INT,
    productname VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    unitprice DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    currentstock INT NOT NULL DEFAULT 0,
    reorderlevel INT NOT NULL DEFAULT 10,
    CONSTRAINT fk_supplier
        FOREIGN KEY(supplierid) 
        REFERENCES suppliers(supplierid)
        ON DELETE SET NULL
);

CREATE TABLE salestransactions (
    saleid SERIAL PRIMARY KEY,
    productid INT NOT NULL,
    quantitysold INT NOT NULL,
    saleprice DECIMAL(10, 2) NOT NULL,
    saledate TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT fk_product_sale
        FOREIGN KEY(productid) 
        REFERENCES products(productid)
        ON DELETE CASCADE
);

CREATE TABLE demandpredictions (
    predictionid SERIAL PRIMARY KEY,
    productid INT NOT NULL,
    predicteddemand INT NOT NULL,
    predictionstartdate DATE NOT NULL,
    predictionenddate DATE NOT NULL,
    modelused VARCHAR(50) NOT NULL,
    CONSTRAINT fk_product_prediction
        FOREIGN KEY(productid) 
        REFERENCES products(productid)
        ON DELETE CASCADE
);