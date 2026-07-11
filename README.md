# User/Post Flask API

Mock API which allows one to send data to a Flask app as a user or a post from a user.

## Technology Used
- Flask
- SQLite
- Flask-Limiter

## How to Run

1. Create a virtual environment (venv) on your machine and activate it
```bash
   mkdir my-api && cd my-api
   python3 -m venv venv
   source venv/bin/activate   # on Windows: venv\Scripts\activate
```

2. Install requirements through terminal
```bash
   pip install -r requirements.txt
```

3. Create a database using schema.sql through terminal
```bash
   sqlite3 database.db < schema.sql
```

4. Run app.py through terminal
```bash
   python3 app.py
```

## Endpoints

### `GET /`
Uses the `home()` function to return `{"message": "API is alive"}`

### `GET /hello/<name>`
Uses the `hello(name)` function and returns `{"greeting": f"Hello, {name}!"}` using the name parameter provided.

**Example:** `/hello/Daniel` returns `{"greeting": "Hello, Daniel!"}`

### `POST /echo`
Uses the `echo()` function to return whatever data is sent.

**Example:**
```bash
curl -X POST http://127.0.0.1:5000/echo -H "Content-Type: application/json" -d '{"Hello": "world!"}'
```
Returns:
```json
{
  "you sent": {
    "Hello": "world!"
  }
}
```

### `GET /users`
Uses the `get_users()` function to connect to the database and retrieve all users created through `POST /users`.

**Example:** (assuming a user with username "Jason" and email "jason@propemail.com" was added)
```json
{
  "users": [
    {
      "created_at": "TIMESTAMP CREATED",
      "email": "jason@propemail.com",
      "id": "(user id)",
      "username": "jason"
    }
  ]
}
```

### `POST /users`
Uses the `create_user()` function to add a user to the database.

- Returns `{"message": "User created successfully", "username": username}` with code **201** if the user is successfully created
- Returns `{"error": "username or email already exists"}` with code **409** if the username/email is already taken

**Example:**
```bash
curl -X POST http://127.0.0.1:5000/users -H "Content-Type: application/json" -d '{"username": "Jason", "email": "jason@propemail.com"}'
```

### `GET /posts`
Uses the `get_posts()` function to retrieve posts from the database.

**Example:** (assuming a post with title "First Post" and content "This is my first ever post!" was created)
```json
{
  "posts": [
    {
      "content": "This is my first ever post!",
      "created_at": "TIMESTAMP CREATED",
      "id": "(post id)",
      "title": "First Post",
      "user_id": "(user id)"
    }
  ]
}
```

### `POST /posts`
Uses the `create_post()` function to add a post to the database.

- Returns `{"message": "Post created", "title": title}` with code **201** if the insertion is successful
- Returns `{"error": "user id, title, and content are required"}` with code **400** if any field is missing
- Returns `{"error": "Invalid User ID"}` with code **404** if the `user_id` doesn't exist

**Example:**
```bash
curl -X POST http://127.0.0.1:5000/posts -H "Content-Type: application/json" -d '{"user_id": 1, "title": "Second Post", "content": "Testing the API"}'
```

## Notes
- `POST /users` and `POST /posts` are rate-limited to 5 requests per minute per IP address.
- Foreign key constraints must be explicitly enabled per connection in SQLite (`PRAGMA foreign_keys = ON`) — they are not enforced by default.