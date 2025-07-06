# Hottracks Inventory Management

This project provides a simple inventory management API for Kyobo Bookstore's Hottracks electronics section. It is built with **FastAPI** and uses a lightweight SQLite database.

Features include:

- Basic CRUD operations for inventory items.
- Recording daily sales history.
- AI-powered sales forecasting using scikit-learn.

## Setup

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

Run the development server:

```bash
uvicorn inventory_app.main:app --reload
```

## Usage

The API offers the following endpoints:

- `GET /items` – list items in inventory
- `POST /items` – add a new item
- `PUT /items/{id}` – update an item
- `DELETE /items/{id}` – remove an item
- `POST /items/{id}/sales` – record units sold today
- `GET /forecast/{id}` – predict next day's sales for an item

The server automatically seeds the database with a few sample items on first run.
