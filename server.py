from flask import Flask, redirect, url_for, request, render_template
import sqlite3

app = Flask(__name__)

@app.route("/")
def index():
    return redirect("/home")

@app.route("/home")
def home():
    return render_template("home.html")

db = sqlite3.connect('database.db')
db.execute('CREATE TABLE IF NOT EXISTS CHARACTERS (name TEXT, hp TEXT)')

@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['user']
        return redirect(url_for('characters', name = user))
    else:
        return render_template("login.html")

@app.route("/characters/<name>", methods=['POST', 'GET'])
def characters(name):
    if request.method == 'POST':
        hp = request.form['hp'].replace(' ', '')
        with sqlite3.connect("database.db") as users:
            cursor = users.cursor()
            if cursor.execute("SELECT * FROM CHARACTERS WHERE name=\'" + name + "\'").fetchall():
                cursor.execute("UPDATE CHARACTERS SET hp = \'" + hp + "\' WHERE name=\'" + name + "\'")
            else:
                cursor.execute("INSERT INTO CHARACTERS (name,hp) VALUES (?,?)", (name, hp))
            users.commit()
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM CHARACTERS WHERE name=\'" + name + "\'")
    data = cursor.fetchall()
    if not data:
        data = [('0','0')]
    print(data)
    return render_template("sheet.html",name = name, character = data)

if __name__ == "__main__":
    app.run()
