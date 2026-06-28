import os
import json
import random
from cs50 import SQL
from flask import Flask, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Connect to SQLite database
db = SQL("sqlite:///match_it.db")

# ---------------------------------------------------------------------------
# DATABASE INITIALISATION
# Creates tables on first run if they do not exist.
# ---------------------------------------------------------------------------
def init_db():
    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT    NOT NULL UNIQUE,
            hash     TEXT    NOT NULL
        )
    """)
    db.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id    INTEGER NOT NULL,
            accuracy   REAL    NOT NULL,
            played_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    db.execute("""
        CREATE TABLE IF NOT EXISTS images (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            filename     TEXT NOT NULL,
            target_hex   TEXT NOT NULL,
            label        TEXT
        )
    """)

init_db()

# ---------------------------------------------------------------------------
# HELPER: Generate distractor colors
# ---------------------------------------------------------------------------
def generate_distractors(target_hex, count=5):
    """
    Given a target color in hex format (e.g. '#F4A460'),
    return `count` hex colors that are visually similar but NOT identical.

    TODO (TASK 4 - BONUS):
    -------------------------
    Currently this function returns random colors — they are not similar to
    the target at all, making the game too easy to cheat.

    Your job is to implement a proper algorithm:
      1. Parse target_hex into R, G, B integer components.
      2. For each distractor, randomly offset each channel by ±15–60 units
         (clamp between 0–255 so values don't overflow).
      3. Make sure no generated color is within ±5 units on ALL channels
         simultaneously (i.e., it must differ enough to not be the same).
      4. Return the results as a list of hex strings like ['#F0A040', ...].

    Hint: Use Python's random.randint() and string formatting:
        hex_str = '#{:02X}{:02X}{:02X}'.format(r, g, b)
    """
    # PLACEHOLDER — replace this entire block with your algorithm
    distractors = []
    while len(distractors) < count:
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        distractors.append('#{:02X}{:02X}{:02X}'.format(r, g, b))
    return distractors


# ---------------------------------------------------------------------------
# AUTH ROUTES
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username or not password or not confirmation:
            return render_template("register.html", error="All fields are required.")
        if password != confirmation:
            return render_template("register.html", error="Passwords do not match.")

        existing = db.execute("SELECT id FROM users WHERE username = ?", username)
        if existing:
            return render_template("register.html", error="Username already taken.")

        db.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?)",
            username,
            generate_password_hash(password)
        )
        rows = db.execute("SELECT id FROM users WHERE username = ?", username)
        session["user_id"] = rows[0]["id"]
        session["username"] = username
        return redirect("/game")
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return render_template("index.html", error="Invalid username or password.")
        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]
        return redirect("/game")
    return render_template("index.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ---------------------------------------------------------------------------
# GAME ROUTES
# ---------------------------------------------------------------------------
@app.route("/game")
def game():
    if not session.get("user_id"):
        return redirect("/")
    # Initialise round tracking in session
    session["round"] = 1
    session["correct"] = 0
    return render_template("game.html", username=session["username"])


@app.route("/game/next", methods=["GET"])
def game_next():
    """
    Returns JSON for the current round:
      {
        "round":       <int 1-5>,
        "image_url":   <string>,
        "swatches":    ["#HEX", "#HEX", "#HEX", "#HEX", "#HEX", "#HEX"],
        "answer_index": <int 0-5>   <- index of correct swatch
      }

    TODO (TASK 1):
    -------------------------
    1. Check that session["round"] is between 1 and 5. If > 5, return
       JSON {"done": true} so game.js knows to redirect to /results.
    2. Query the `images` table to get a RANDOM image row:
           SELECT * FROM images ORDER BY RANDOM() LIMIT 1
    3. Call generate_distractors(row["target_hex"]) to get 5 wrong colors.
    4. Build a list of 6 swatches by inserting the correct target_hex at a
       random index (0-5) among the 5 distractors.
    5. Return jsonify({...}) with the fields described above.
    """
    # TODO: replace this placeholder response
    return jsonify({"error": "Not implemented yet"}), 501


@app.route("/game/submit", methods=["POST"])
def game_submit():
    """
    Receives JSON from the front-end:
      { "selected_index": <int>, "answer_index": <int> }

    Returns JSON:
      { "correct": <bool>, "round": <int>, "done": <bool> }

    TODO (TASK 2):
    -------------------------
    1. Parse the JSON body from request.get_json().
    2. Compare selected_index == answer_index to determine correctness.
    3. If correct, increment session["correct"] by 1.
    4. Increment session["round"] by 1.
    5. If session["round"] > 5 (all rounds done):
       a. Calculate accuracy = (session["correct"] / 5) * 100
       b. Save to the `scores` table:
              INSERT INTO scores (user_id, accuracy) VALUES (?, ?)
       c. Store accuracy in session["last_accuracy"] for the results page.
       d. Return jsonify({"correct": ..., "round": 5, "done": True})
    6. Otherwise return jsonify({"correct": ..., "round": session["round"], "done": False})
    """
    # TODO: replace this placeholder response
    return jsonify({"error": "Not implemented yet"}), 501


@app.route("/results")
def results():
    if not session.get("user_id"):
        return redirect("/")
    accuracy = session.get("last_accuracy", 0)
    # Fetch top 10 leaderboard scores
    leaderboard = db.execute("""
        SELECT users.username, scores.accuracy, scores.played_at
        FROM scores
        JOIN users ON scores.user_id = users.id
        ORDER BY scores.accuracy DESC
        LIMIT 10
    """)
    return render_template("results.html",
                           accuracy=accuracy,
                           leaderboard=leaderboard,
                           username=session["username"])
