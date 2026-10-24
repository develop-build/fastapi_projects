from fastapi import FastAPI, Query

app = FastAPI(title = "Search and Filter API")

products = [
    {"id" : 1, "name" : "Laptop", "category" : "Electronics", "price" : 50000},
    {"id" : 2, "name" : "Mouse", "category" : "Electronics", "price" : 2000},
    {"id" : 3, "name" : "Mobile", "category" : "Electronics", "price" : 1000},
    {"id" : 4, "name" : "Keyboard", "category" : "Electronics", "price" : 3000},
    {"id" : 5, "name" : "Monitor", "category" : "Electronics", "price" : 10000},
    {"id" : 6, "name" : "T-Shirt", "category" : "Clothing", "price" : 500},
    {"id" : 7, "name" : "Jeans", "category" : "Clothing", "price" : 1000},
]

@app.get("/products")
def get_products(
    q: str | None = Query(default=None),
    category: str | None = Query(default = None),
    min_price: float | None = Query(default = None, ge=0),
    max_price: float | None = Query(default = None, ge=0),
    limit: int = Query(default=10,ge=1, le=100),
    offset: int = Query(default = 0, ge=0),
    sort_by: str = Query(default="id", pattern="^(id|name|price)$"),
    order: str = Query(default="asc", pattern="^(asc|desc)$"),
):
    result = products

    if q is not None:
       result = [
        product
        for product in result
        if q.lower() in product["name"].lower()
    ]

    if category is not None:
        result = [
            product
            for product in result
            if product["category"].lower() == category.lower()
        ]
    
    if min_price is not None:
        result = [
            product for product in result
            if(product["price"] >= min_price)
        ]
    if max_price is not None:
        result = [
            product for product in result
            if(product["price"] <= max_price)
        ]

    result = sorted(
        result,
        key=lambda product: product[sort_by],
        reverse=(order == "desc")
    )

    return result[offset:offset + limit]