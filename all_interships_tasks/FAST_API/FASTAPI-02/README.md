# FastAPI Day 2 Assignment

This project contains the `main.py` implementation for the FastAPI Day 2 assignment (products, feedback, orders, bulk orders, and order tracking).

## Install dependencies

```bash
pip install -r requirements.txt
```

## Run the server

From the `fastapi2` folder:

```bash
uvicorn main:app --reload
```

Open the browser:

- Swagger UI (for POST endpoints and screenshots): http://127.0.0.1:8000/docs
- Test GET URLs directly in browser (for Q1, Q2, Q4, etc.)

## Endpoints (mapping to questions)

- Q1: `GET /products/filter` with `min_price`, `max_price`, `category`
- Q2: `GET /products/{product_id}/price`
- Q3: `POST /feedback`
- Q4: `GET /products/summary`
- Q5: `POST /orders/bulk`
- Bonus: `POST /orders`, `GET /orders/{order_id}`, `PATCH /orders/{order_id}/confirm`

