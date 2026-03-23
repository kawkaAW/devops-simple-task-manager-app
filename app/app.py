from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import os
import time

app = Flask(__name__)


def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "db"),
        database=os.getenv("POSTGRES_DB", "taskdb"),
        user=os.getenv("POSTGRES_USER", "taskuser"),
        password=os.getenv("POSTGRES_PASSWORD", "taskpassword"),
        port=os.getenv("POSTGRES_PORT", "5432")
    )
    return conn


def init_db():
    max_retries = 10
    retry_delay = 3

    for attempt in range(max_retries):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(255) NOT NULL
                );
            """)
            conn.commit()
            cur.close()
            conn.close()
            print("Database initialized successfully.")
            return
        except Exception as e:
            print(f"Database connection failed (attempt {attempt + 1}/{max_retries}): {e}")
            time.sleep(retry_delay)

    raise Exception("Could not connect to the database after multiple attempts.")


@app.route("/")
def home():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, title FROM tasks ORDER BY id;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    tasks = [{"id": row[0], "title": row[1]} for row in rows]
    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("title")

    if title and title.strip():
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO tasks (title) VALUES (%s);", (title.strip(),))
        conn.commit()
        cur.close()
        conn.close()

    return redirect(url_for("home"))


@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id = %s;", (task_id,))
    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for("home"))


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)