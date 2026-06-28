# Match It 🎨

## CS50 Final Project — Distribution Code

Match It is a color memory game. An image is shown for 10 seconds; after it disappears, you must identify the exact color from the image out of 6 similar-looking swatches. You play 5 rounds and receive an accuracy rating.

---

## Project Structure

```
match_it/
├── app.py                  # Flask backend (INCOMPLETE - see TODOs)
├── match_it.db             # SQLite database (created on first run)
├── requirements.txt        # Python dependencies
├── static/
│   ├── style.css           # Styles (INCOMPLETE - see TODOs)
│   ├── game.js             # Game logic (INCOMPLETE - see TODOs)
│   └── images/             # Folder for cartoon images
│       └── .gitkeep
└── templates/
    ├── layout.html         # Base HTML layout
    ├── index.html          # Home / login page
    ├── register.html       # Registration page
    ├── game.html           # Main game screen
    └── results.html        # Results / leaderboard page
```

---

## Setup Instructions

```bash
pip install -r requirements.txt
flask run
```

---

## What You Need to Implement

See the `TODO` comments inside each file. The main tasks are:

1. **`app.py`** — Write the `/game/next` route that fetches a round's image + target color from the DB, and the `/game/submit` route that checks the user's answer and saves the score.
2. **`game.js`** — Implement the 10-second countdown timer, image hide logic, and the `fetch` call to submit the user's answer asynchronously.
3. **`style.css`** — Style the color swatch buttons and animate the countdown timer bar.
4. **`app.py` (bonus)** — Implement the color distractor generation algorithm (`generate_distractors`) that produces 5 visually similar but distinct colors.

---

## Design Choices (for your README submission)

Describe here why you chose Flask over Django, how you structured your SQL schema, and how you approached the color similarity algorithm.
