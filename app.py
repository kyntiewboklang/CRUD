from flask import Flask, render_template, request, redirect
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

@app.route("/add-book", methods=["GET","POST"])
def add_book():
    if request.method=="POST":
        title = request.form["title"]
        author = request.form["author"]
        category = request.form["category"]
        status = request.form["status"]

        print(title, author, category, status)

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
                       INSERT INTO books (title, author, category, status)
                       VALUES (%s, %s, %s, %s)
                       """ , (title, author, category, status))
        
        conn.commit()
        cursor.close()
        conn.close()

        return redirect("/view_book")
    return render_template("add_book.html")

@app.route("/view_book")
def view_book():
    conn = get_db_connection()
    cursor = conn.cursor() 

    cursor.execute("SELECT * FROM books ORDER BY id ASC")
    books = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("view_book.html", books=books)

if __name__ == "__main__":  #important code, it is use for running the app
    create_table() 
    app.run(debug=True)