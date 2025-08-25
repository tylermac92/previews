from fastapi import FastAPI
import os, psycopg2

app = FastAPI()

def db_check():
    dsn = os.getenv("DATABASE_URL")
    if not dsn:
        return {"connected": False, "reason": "no DATABASE_URL"}
    try:
        with psycopg2.connect(dsn) as conn:
            with conn.cursor() as cur:
                cur.execute("select 'ok'::text,")
                return {"connected": True, "dsn": dsn}
    except Exception as e:
        return {"connected": False, "reason": str(e)}

@app.get("/")
def read_root():
    return {"service": "myapp", "env": os.getenv("APP_ENV", "local")}

@app.get("/healthz")
def healthz():
    return {"ok": True}

@app.get("/db")
def db():
    return db_check()
