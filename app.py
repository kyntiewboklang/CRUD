from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash,check_password_hash 
import psycopg2

app = Flask(__name__)

app.secret_key="your_secret_key_here"

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

def create_user():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            password VARCHAR(255) NOT NULL
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()

    print("users table created successfully")

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM users
            WHERE username=%s
        """, (username,))

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user and check_password_hash(user[3], password):
            session["user_id"] = user[0]
            session["username"] = user[1]
            session["email"] = user[2]
            return redirect("/home")

        return "Invalid credentials"

    return render_template("login.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method=="POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password=request.form["confirm_password"]
        if password!=confirm_password:
            return "Password does not match"

        hashed_password = generate_password_hash(password)

        print(username, email, password)

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
                       INSERT INTO users (username, email, password)
                       VALUES (%s, %s, %s)
                       """ , (username, email,hashed_password))
        
        conn.commit()
        cursor.close()
        conn.close()

        print("User registration successful")
    return render_template("register.html")

@app.route("/forget_password", methods=["GET", "POST"])
def forget_password():
    
    message = ""
    category = ""

    if request.method == "POST":
        email = request.form["email"]

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * 
            FROM users
            WHERE email = %s
        """, (email,))

        user = cursor.fetchone()

        conn.commit()
        conn.close()

        if user:
            return redirect(f"/reset-password/{email}")
        else:
            message = "User does not have an account."
            category = "danger"

    return render_template("forget_password.html", message=message, category=category)

@app.route("/reset-password/<email>", methods=["GET", "POST"])
def reset_password(email):
    if request.method == "POST":
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]

        if new_password != confirm_password:
            return "Password does not match"
        
        hashed_password = generate_password_hash(new_password)

        conn = get_db_connection()
        cursor = conn.cursor() 

        cursor.execute("""
            UPDATE users SET password = %s WHERE email =%s
                    """, (hashed_password, email))
        
        conn.commit()
        cursor.close()
        conn.close()

        return redirect("/")

    return render_template("reset_password.html")

@app.route("/home")
def home():

    if "user_id" not in session:
        return redirect("/")

    return render_template("index.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")



@app.route("/add-book", methods=["GET","POST"])
def add_book():
    if "user_id" not in session:
        return redirect("/")

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
    if "user_id" not in session:
        return redirect("/")


    conn = get_db_connection()
    cursor = conn.cursor() 

    cursor.execute("SELECT * FROM books ORDER BY id ASC")
    books = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("view_book.html", books=books)

@app.route("/delete-book/<int:id>")
def delete_book(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM books WHERE id =%s", (id,))
    
    conn.commit()

    cursor.close()
    conn.close()

    return redirect("/view_book")

@app.route("/edit-book/<int:id>", methods=["GET", "POST"])
def edit_book(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        category = request.form["category"]
        status = request.form["status"]

        cursor.execute("""
            UPDATE books
            SET title=%s,
                author=%s,
                category=%s,
                status=%s
            WHERE id=%s
        """, (title, author, category, status, id))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect("/view_book")

    cursor.execute("SELECT * FROM books WHERE id = %s", (id,))
    book = cursor.fetchone()

    cursor.close()
    conn.close()

    if book is None:
        return "Book not found", 404

    return render_template("add_book.html", book=book)



if __name__ == "__main__":  #important code, it is use for running the app
    create_table() 
    create_user()
    print(app.url_map)
    app.run(debug=True)