import sqlite3
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return {"message": "API is alive"}

@app.route("/hello/<name>")
def hello(name):
    return {"greeting": f"Hello, {name}!"}


@app.route("/echo", methods=["POST"])
def echo():
    data = request.get_json()
    return {"you sent": data}

@app.route('/users', methods=['GET'])
def get_users():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    rows = cursor.fetchall()
    conn.close()

    users = [dict(row) for row in rows]
    return {"users": users}

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    if username is None or email is None:
        return {"error": "username and email are required"}, 400
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (username, email) VALUES (?, ?)', (username, email))
        conn.commit()
        conn.close()
        return {"message": "User created successfully", "username": username}, 201
    except sqlite3.IntegrityError:
        conn.close()
        return {"error": "username or email already exists"}, 409


@app.route('/posts', methods=['GET'])
def get_posts():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM posts')
    rows = cursor.fetchall()
    conn.close()

    posts = [dict(row) for row in rows]
    return {"posts": posts}

@app.route("/posts", methods=["POST"])
def create_post():
    data = request.get_json()
    user_id = data.get("user_id")
    title = data.get("title")
    content = data.get("content")
    if title is None or content is None or user_id is None:
        return {"error": "user id, title, and content are required"}, 400
    conn = sqlite3.connect("database.db")
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO posts (user_id, title, content) VALUES (?, ?, ?)", (user_id, title, content))
        conn.commit()
        conn.close()
        return {"message": "Post created", "title": title}, 201
    except sqlite3.IntegrityError:
        conn.close()
        return {"error": "Invalid User ID"}, 400

if __name__ == '__main__':
    app.run(debug=True)


