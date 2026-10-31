from fastapi import FastAPI, Query

app = FastAPI(title="Page Sorting API")

@app.get("/health")
def get_health():
    return {"status": "ok"}

items = [
    {"id": 1, "name": "Laptop"},
    {"id": 2, "name": "Mouse"},
    {"id": 3, "name": "Keyboard"},
    {"id": 4, "name": "Monitor"},
    {"id": 5, "name": "Headphones"}
]

@app.get("/items")
def get_items(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=1, ge=1, le=100),
    sort_by: str = Query(default="name", pattern="^(name|id)$"),
    order: str = Query(default="asc", pattern="^(asc|desc)$"),
):
    sorted_items = sorted(
        items,
        key=lambda item: item[sort_by],
        reverse=(order == "desc")
    )
    paginated_items = sorted_items()
    return {
        "total": len(items),
        "skip": skip,
        "limit": limit,
        "items": items[skip: skip+limit]
    }
