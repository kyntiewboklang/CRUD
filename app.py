from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add-book")
def add_book():
    return render_template("add_book.html")

if __name__ == "__main__":  #important code, it is use for running the app
    app.run(debug=True)