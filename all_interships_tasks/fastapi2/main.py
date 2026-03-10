from typing import List, Optional

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI(title="FastAPI Day 2 Assignment")


# In-memory data
products = [
    {
        "id": 1,
        "name": "Wireless Mouse",
        "category": "Electronics",
        "price": 499,
        "in_stock": True,
    },
    {
        "id": 2,
        "name": "Notebook",
        "category": "Stationery",
        "price": 99,
        "in_stock": True,
    },
    {
        "id": 3,
        "name": "USB Hub",
        "category": "Electronics",
        "price": 799,
        "in_stock": False,
    },
    {
        "id": 4,
        "name": "Pen Set",
        "category": "Stationery",
        "price": 49,
        "in_stock": True,
    },
]

orders: List[dict] = []
feedback: List[dict] = []


@app.get("/")
def read_root():
    return {"message": "FastAPI Day 2 Assignment - Products & Orders API"}


# Q1 - Extend /products/filter with min_price
@app.get("/products/filter")
def filter_products(
    category: Optional[str] = Query(
        None, description="Filter products by category (e.g. Electronics)"
    ),
    max_price: Optional[int] = Query(
        None, description="Maximum price of product"
    ),
    min_price: Optional[int] = Query(
        None, description="Minimum price of product"
    ),
):
    result = products.copy()

    if category:
        result = [
            p for p in result if p["category"].lower() == category.lower()
        ]

    if max_price is not None:
        result = [p for p in result if p["price"] <= max_price]

    if min_price is not None:
        result = [p for p in result if p["price"] >= min_price]

    return {"products": result}


# Q2 - Get only the price of a product
@app.get("/products/{product_id}/price")
def get_product_price(product_id: int):
    product = next((p for p in products if p["id"] == product_id), None)
    if not product:
        return {"error": "Product not found"}
    return {"name": product["name"], "price": product["price"]}


# Q3 - Accept customer feedback
class CustomerFeedback(BaseModel):
    customer_name: str = Field(..., min_length=2, max_length=100)
    product_id: int = Field(..., gt=0)
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = Field(None, max_length=300)


@app.post("/feedback")
def submit_feedback(data: CustomerFeedback):
    feedback_entry = data.dict()
    feedback.append(feedback_entry)
    return {
        "message": "Feedback submitted successfully",
        "feedback": feedback_entry,
        "total_feedback": len(feedback),
    }


# Q4 - Product summary dashboard
@app.get("/products/summary")
def product_summary():
    in_stock = [p for p in products if p["in_stock"]]
    out_stock = [p for p in products if not p["in_stock"]]

    most_expensive = max(products, key=lambda p: p["price"])
    cheapest = min(products, key=lambda p: p["price"])

    categories = list({p["category"] for p in products})

    return {
        "total_products": len(products),
        "in_stock_count": len(in_stock),
        "out_of_stock_count": len(out_stock),
        "most_expensive": {
            "name": most_expensive["name"],
            "price": most_expensive["price"],
        },
        "cheapest": {"name": cheapest["name"], "price": cheapest["price"]},
        "categories": categories,
    }


# Q5 - Bulk order models and endpoint
class OrderItem(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0, le=50)


class BulkOrder(BaseModel):
    company_name: str = Field(..., min_length=2)
    contact_email: str = Field(..., min_length=5)
    items: List[OrderItem] = Field(..., min_items=1)


@app.post("/orders/bulk")
def place_bulk_order(order: BulkOrder):
    confirmed: List[dict] = []
    failed: List[dict] = []
    grand_total = 0

    for item in order.items:
        product = next((p for p in products if p["id"] == item.product_id), None)

        if not product:
            failed.append(
                {
                    "product_id": item.product_id,
                    "reason": "Product not found",
                }
            )
            continue

        if not product["in_stock"]:
            failed.append(
                {
                    "product_id": item.product_id,
                    "reason": f"{product['name']} is out of stock",
                }
            )
            continue

        subtotal = product["price"] * item.quantity
        grand_total += subtotal
        confirmed.append(
            {
                "product": product["name"],
                "qty": item.quantity,
                "subtotal": subtotal,
            }
        )

    return {
        "company": order.company_name,
        "confirmed": confirmed,
        "failed": failed,
        "grand_total": grand_total,
    }


# Bonus - basic order placement + tracking
class SimpleOrder(BaseModel):
    customer_name: str = Field(..., min_length=2)
    items: List[OrderItem] = Field(..., min_items=1)


@app.post("/orders")
def place_order(order: SimpleOrder):
    total_amount = 0
    order_items: List[dict] = []

    for item in order.items:
        product = next((p for p in products if p["id"] == item.product_id), None)
        if not product or not product["in_stock"]:
            return {
                "error": f"Product with id {item.product_id} not available for ordering"
            }

        subtotal = product["price"] * item.quantity
        total_amount += subtotal
        order_items.append(
            {
                "product": product["name"],
                "qty": item.quantity,
                "subtotal": subtotal,
            }
        )

    order_id = len(orders) + 1
    order_record = {
        "order_id": order_id,
        "customer_name": order.customer_name,
        "items": order_items,
        "total_amount": total_amount,
        "status": "pending",
    }
    orders.append(order_record)

    return {"message": "Order placed successfully", "order": order_record}


@app.get("/orders/{order_id}")
def get_order(order_id: int):
    order = next((o for o in orders if o["order_id"] == order_id), None)
    if not order:
        return {"error": "Order not found"}
    return {"order": order}


@app.patch("/orders/{order_id}/confirm")
def confirm_order(order_id: int):
    order = next((o for o in orders if o["order_id"] == order_id), None)
    if not order:
        return {"error": "Order not found"}

    order["status"] = "confirmed"
    return {"message": "Order confirmed", "order": order}

