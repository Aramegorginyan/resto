from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# Database setup
conn = sqlite3.connect('pizza_menu.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS pizzas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        description TEXT,
        price FLOAT
    )
''')
conn.commit()

# Pydantic model for request payload
class Pizza(BaseModel):
    name: str
    description: str
    price: float

# Create Operation (C)
@app.post("/pizzas/")
async def create_pizza(pizza: Pizza):
    cursor.execute('''
        INSERT INTO pizzas (name, description, price) VALUES (?, ?, ?)
    ''', (pizza.name, pizza.description, pizza.price))
    conn.commit()
    return {"message": "Pizza added successfully"}

# Read Operation (R)
@app.get("/pizzas/")
async def get_pizzas():
    cursor.execute('SELECT * FROM pizzas')
    pizzas = cursor.fetchall()
    return {"pizzas": pizzas}

# Update Operation (U)
@app.put("/pizzas/{pizza_id}")
async def update_pizza(pizza_id: int, pizza: Pizza):
    cursor.execute('''
        UPDATE pizzas SET name=?, description=?, price=? WHERE id=?
    ''', (pizza.name, pizza.description, pizza.price, pizza_id))
    conn.commit()
    return {"message": "Pizza updated successfully"}

# Delete Operation (D)
@app.delete("/pizzas/{pizza_id}")
async def delete_pizza(pizza_id: int):
    cursor.execute('DELETE FROM pizzas WHERE id=?', (pizza_id,))
    conn.commit()
    return {"message": "Pizza deleted successfully"}
