from fastapi import FastAPI, HTTPException
import redis
import psycopg2
import os

app = FastAPI()

# -------------------
# Redis Initialization
# -------------------
try:
    r = redis.Redis(host="redis", port=6379, decode_responses=True)  # decode_responses=True returns string instead of bytes
    r.ping()  # test connection
except redis.exceptions.ConnectionError as e:
    print("Redis connection failed:", e)
    r = None

# -------------------
# Postgres Initialization
# -------------------
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host="db",
            database=os.getenv("POSTGRES_DB", "demo"),
            user=os.getenv("POSTGRES_USER", "demo"),
            password=os.getenv("POSTGRES_PASSWORD", "password"),
        )
        return conn
    except Exception as e:
        print("Postgres connection failed:", e)
        return None


# -------------------
# Redis Endpoints
# -------------------
@app.get("/cache/{key}")
def cache_get(key: str):
    if not r:
        raise HTTPException(status_code=500, detail="Redis not available")
    val = r.get(key)
    if val is None:
        raise HTTPException(status_code=404, detail="Key not found")
    return {"key": key, "value": val}


@app.post("/cache/{key}/{value}")
def cache_set(key: str, value: str):
    if not r:
        raise HTTPException(status_code=500, detail="Redis not available")
    try:
        r.set(key, value)
        return {"status": "ok", "key": key, "value": value}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to set key: {e}")


# -------------------
# Postgres Example Endpoint
# -------------------
@app.get("/db-test")
def db_test():
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Postgres not available")
    cur = conn.cursor()
    cur.execute("SELECT version();")
    version = cur.fetchone()
    cur.close()
    conn.close()
    return {"postgres_version": version}


@app.get("/")
def root():
    return {"message": "Hello from Bootcamp Day 3"}
