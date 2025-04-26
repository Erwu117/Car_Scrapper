# Run 'python fetch.py' once to fetch data
from connect import connect
from config import load_config
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, Query, HTTPException

# https://neon.tech/guides/fastapi-async
app = FastAPI()

@app.get("/price-range/")
def get_price_range(model:str):
    config = load_config()
    conn = connect(config)
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT MIN(price), MAX(price)
            FROM cartests
            WHERE title ILIKE %s
        """, (f"%{model}%",))
        result = cur.fetchone()
        if result and result[0] is not None:
            return{
                "model": model,
                "min_price": result[0],
                "max_price": result[1]
            }
        else:
            return {"model": model, "message": "No matching cars"}
    finally:
        cur.close()
        conn.close()

@app.get("/most-selling/")
def get_most_selling(month:int):
    config = load_config()
    conn = connect(config)
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT title, COUNT(*) AS car_total
            FROM cartests
            WHERE EXTRACT(MONTH FROM date_listed) = %s
            GROUP BY title
            ORDER BY car_total DESC
            LIMIT 1
        """, (month,))
        result = cur.fetchone()
        if result: 
            return{
                "month":month,
                "most_selling_car": result[0]
            }
        else:
            return {"month": month, "message": "Not found or Invalid"}
    finally:
        cur.close()
        conn.close()

@app.get("/least-selling/")
def get_top_selling(month:int):
    config = load_config()
    conn = connect(config)
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT title, COUNT(*) AS car_total
            FROM cartests
            WHERE EXTRACT(MONTH FROM date_listed) = %s
            GROUP BY title
            ORDER BY car_total ASC
            LIMIT 1
        """, (month,))
        result = cur.fetchone()
        if result: 
            return{
                "month":month,
                "least_selling_car": result[0]
            }
        else:
            return {"month": month, "message": "Not found or Invalid"}
    finally:
        cur.close()
        conn.close()