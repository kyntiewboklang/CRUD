from flask import Flask, render_template
import psycopg2

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="library_db",
        username="postgres",
        password="1234"
    )

    return conn

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
    app.run(debug=True)