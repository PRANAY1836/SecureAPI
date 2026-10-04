from flask import Flask, request
from database import get_connection, initialize_database
from werkzeug.security import check_password_hash
from functools import wraps
import jwt
from datetime import datetime, timedelta, timezone
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

app = Flask(__name__)

limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=[]
)

@app.after_request
def add_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return {"error": "Token is missing"}, 401

        try:
            token = token.replace("Bearer ", "")
            decoded = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=["HS256"]
            )
        except jwt.InvalidTokenError:
            return {"error": "Invalid or expired token"}, 401

        return f(decoded, *args, **kwargs)

    return decorated

@app.route("/")
def home():
    return {
        "message": "SecureAPI is running"
    }


@app.route("/api/users")
def get_users():
    connection = get_connection()

    users = connection.execute(
        "SELECT id, name, email FROM users"
    ).fetchall()

    connection.close()

    return [dict(user) for user in users]

@app.route("/api/users/<int:user_id>")
@token_required
def get_user(decoded_token, user_id):

    if decoded_token["user_id"] != user_id:
        return {"error": "Access denied"}, 403

    connection = get_connection()

    user = connection.execute(
        "SELECT id, name, email FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()

    connection.close()

    if user is None:
        return {"error": "User not found"}, 404

    return dict(user)

@app.route("/api/login", methods=["POST"])
@limiter.limit("5 per minute")
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")


    connection = get_connection()

    user = connection.execute(
        "SELECT * FROM users WHERE email = ?",
        (email,)
    ).fetchone()

    connection.close()

    if user is None:
        return {"error": "Invalid credentials"}, 401

    if not check_password_hash(user["password"], password):
        return {"error": "Invalid credentials"}, 401

    token = jwt.encode(
        {
            "user_id": user["id"],
            "email": user["email"],
            "exp": datetime.now(timezone.utc) + timedelta(hours=1)
        },
        SECRET_KEY,
        algorithm="HS256"
    )

    return {
        "message": "Login successful",
        "token": token
    }

@app.route("/api/search")
def search_users():
    name = request.args.get("name", "")

    connection = get_connection()

    query = "SELECT id, name, email FROM users WHERE name = ?"

    users = connection.execute(query, (name,)).fetchall()

    connection.close()

    return [dict(user) for user in users]

if __name__ == "__main__":
    initialize_database()
    app.run(debug=True)