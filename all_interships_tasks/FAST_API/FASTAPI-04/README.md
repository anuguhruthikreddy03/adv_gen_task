# FastAPI Day 5 — Cart System (Assignment 4)

## Run the app

```bash
cd c:\Users\anugu\OneDrive\Documents\fastapi_task4
pip install -r requirements.txt
uvicorn main:app --reload
```

Open **Swagger UI**: http://127.0.0.1:8000/docs

## Screenshot checklist

| Question | What to capture |
|----------|-----------------|
| Q1_Output.png | POST /cart/add product_id=1 qty=2 → "Added to cart", subtotal 998; then product_id=2 qty=1 → subtotal 99 |
| Q2_Output.png | GET /cart → item_count: 2, grand_total: 1097 |
| Q3_Output.png | POST /cart/add product_id=3 → 400 "USB Hub is out of stock"; product_id=99 → 404; GET /cart still 2 items |
| Q4_Output.png | POST /cart/add product_id=1 qty=1 → "Cart updated", qty=3, subtotal 1497; GET /cart grand_total 1596 |
| Q5_Output.png | DELETE /cart/2 → GET /cart (1 item, 1497) → POST /cart/checkout → GET /cart empty → GET /orders |
| Q6_Output.png | Full 2-customer flow; final GET /orders showing 3 orders |
| Bonus (optional) | GET /cart empty → POST /cart/checkout → 400; GET /orders unchanged |


