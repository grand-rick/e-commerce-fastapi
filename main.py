from fastapi import FastAPI
from typing import List
from uuid import uuid4

app = FastAPI()

class Product(BaseModel):
    id: uuid4
    name: str
    price: float
    description: str
    image: str

# In-memory database of products
db: List[Product] = []

@app.get("/api/products", response_model=List[Product])
async def list_products():
    return db

@app.post("/api/products", response_model=Product)
async def create_product(product: Product):
    product.id = uuid4()
    db.append(product)
    return product

@app.get("/api/products/{product_id}", response_model=Product)
async def get_product(product_id: uuid4):
    for product in db:
        if product.id == product_id:
            return product
    return {"error": "Product not found"}

@app.put("/api/products/{product_id}", response_model=Product)
async def update_product(product_id: uuid4, updated_product: Product):
    for product in db:
        if product.id == product_id:
            product.name = updated_product.name
            product.price = updated_product.price
            product.description = updated_product.description
            product.image = updated_product.image
            return product
    return {"error": "Product not found"}

@app.delete("/api/products/{product_id}", response_model=Product)
async def delete_product(product_id: uuid4):
    for product in db:
        if product.id == product_id:
            db.remove(product)
            return {"message": "Product deleted", "product_id": product_id}
    return {"error": "Product not found"}