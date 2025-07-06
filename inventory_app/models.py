from pydantic import BaseModel

class Item(BaseModel):
    id: int | None = None
    name: str
    quantity: int

class ItemCreate(BaseModel):
    name: str
    quantity: int

class ForecastResponse(BaseModel):
    item_id: int
    predicted_sales: float
