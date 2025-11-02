// app.js

const API_URL = 'http://127.0.0.1:8001';

document.addEventListener('DOMContentLoaded', () => {

    const addProductForm = document.getElementById('add-product-form');
    addProductForm.addEventListener('submit', (e) => {
        e.preventDefault(); 
        const name = document.getElementById('product-name').value;
        const stock = document.getElementById('product-stock').value;
        const price = document.getElementById('product-price').value;

        fetch(`${API_URL}/products/add?name=${name}&stock=${stock}&price=${price}`, {
            method: 'POST'
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { 
                    throw new Error(err.detail || `HTTP error! status: ${response.status}`) 
                });
            }
            return response.json();
        })
        .then(data => {
            console.log('Success:', data);
            // --- "ID UNDEFINED" FIX ---
            // Reads the lowercase 'productid'
            alert(`Product added! ID: ${data.productid}`);
            addProductForm.reset();
        })
        .catch(error => {
            console.error('Error:', error);
            alert(`Error adding product: ${error.message}`);
        });
    });

    const recordSaleForm = document.getElementById('record-sale-form');
    recordSaleForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const productId = document.getElementById('sale-product-id').value;
        const quantity = document.getElementById('sale-quantity').value;

        fetch(`${API_URL}/sales/record?product_id=${productId}&quantity=${quantity}`, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            if (data.detail) { 
                alert(`Error: ${data.detail}`);
            } else {
                console.log('Success:', data);
                alert(`Sale recorded! New stock: ${data.new_stock}`);
                recordSaleForm.reset();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert(`Error recording sale: ${error.message}`);
        });
    });

    const runPredictionForm = document.getElementById('run-prediction-form');
    runPredictionForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const productId = document.getElementById('predict-product-id').value;
        alert('Starting prediction... This might take a moment.');

        fetch(`${API_URL}/products/${productId}/predict`, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            if (data.detail) {
                alert(`Error: ${data.detail}`);
            } else {
                console.log('Success:', data);
                alert(`Prediction complete! Predicted demand for next 4 weeks: ${data.predicted_demand_next_4_weeks}`);
                runPredictionForm.reset();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert(`Error running prediction: ${error.message}`);
        });
    });
});