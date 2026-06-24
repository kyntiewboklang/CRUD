from flask import Flask, render_template
import psycopg2

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="library_db",
        user="postgres",
        password="1234"
    )
    return conn

def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books(
            id SERIAL PRIMARY KEY,
            title VARCHAR(100) NOT NULL,
            author VARCHAR(100) NOT NULL,
            category VARCHAR(50) NOT NULL,
            status VARCHAR(50) NOT NULL
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()

    print("Books table created successfully")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add-book")
def add_book():
    return render_template("add_book.html")

@app.route("/view_book")
def view_book():
    return render_template("view_book.html")

if __name__ == "__main__":  #important code, it is use for running the app
    create_table() 
    app.run(debug=True)