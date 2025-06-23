from fastapi import FastAPI
import os
import psycopg2

app = FastAPI()

@app.get("/")
def read_root():
    db_host = os.getenv("POSTGRES_HOST", "localhost")
    db_name = os.getenv("POSTGRES_DB", "mydatabase")
    db_user = os.getenv("POSTGRES_USER", "user")
    db_pass = os.getenv("POSTGRES_PASSWORD", "password")

    try:
        conn = psycopg2.connect(
            host=db_host, dbname=db_name, user=db_user, password=db_pass
        )
        return {"message": "Connected to the database!"}
    except Exception as e:
        return {"error": str(e)}
