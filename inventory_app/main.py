from fastapi import FastAPI, HTTPException
from .database import init_db, get_connection
from .models import Item, ItemCreate, ForecastResponse
from .ml import forecast_sales
import sqlite3
import datetime

app = FastAPI(title="Hottracks Inventory Management")

# initialize database
init_db()

@app.get("/items", response_model=list[Item])
def list_items():
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, name, quantity FROM items")
        rows = cur.fetchall()
        return [Item(id=r[0], name=r[1], quantity=r[2]) for r in rows]

@app.post("/items", response_model=Item)
def add_item(item: ItemCreate):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO items (name, quantity) VALUES (?, ?)", (item.name, item.quantity))
        conn.commit()
        item_id = cur.lastrowid
        return Item(id=item_id, **item.dict())

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: ItemCreate):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("UPDATE items SET name=?, quantity=? WHERE id=?", (item.name, item.quantity, item_id))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Item not found")
        conn.commit()
        return Item(id=item_id, **item.dict())

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM items WHERE id=?", (item_id,))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Item not found")
        conn.commit()
        return {"status": "deleted"}

@app.post("/items/{item_id}/sales")
def add_sales_record(item_id: int, sold: int):
    """Add a sales record for an item."""
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id FROM items WHERE id=?", (item_id,))
        if cur.fetchone() is None:
            raise HTTPException(status_code=404, detail="Item not found")
        cur.execute(
            "INSERT INTO history (item_id, date, sold) VALUES (?, ?, ?)",
            (item_id, datetime.date.today().isoformat(), sold)
        )
        conn.commit()
        return {"status": "recorded"}

@app.get("/forecast/{item_id}", response_model=ForecastResponse)
def forecast(item_id: int):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT sold FROM history WHERE item_id=? ORDER BY date", (item_id,))
        rows = cur.fetchall()
        if not rows:
            raise HTTPException(status_code=404, detail="No history for item")
        history = [r[0] for r in rows]
        predicted = forecast_sales(history)
        return ForecastResponse(item_id=item_id, predicted_sales=predicted)
