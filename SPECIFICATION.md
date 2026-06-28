# Match It — CS50 Final Project Specification

## Overview

Match It is a color memory game built with Flask, JavaScript, SQL, HTML, and CSS.
An image is shown for 10 seconds. After it disappears, the user selects the correct
color from 6 swatches. The game lasts 5 rounds.

**Scoring:** Each round is worth 1 point (correct = 1, wrong = 0). Maximum score is **5 / 5**.

This spec is structured like a CS50 problem set. The distribution code is provided in `app.py`,
`game.js`, and `style.css` with placeholder `TODO` comments. Your job is to implement each task.

---

## Tasks

### Task 1 — `/game/next` route (Python, `app.py`)

Complete the `game_next()` function.

**Requirements:**
- If `session["round"] > 5`, return `{"done": true}`.
- Otherwise, fetch a **random** image row from the `images` table.
- Call `generate_distractors(target_hex)` to get 5 wrong colors.
- Insert the correct `target_hex` at a **random** position (0–5) in the list.
- Return JSON with keys: `round`, `image_url`, `swatches`, `answer_index`.

---

### Task 2 — `/game/submit` route (Python, `app.py`)

Complete the `game_submit()` function.

**Requirements:**
- Parse incoming JSON: `selected_index` and `answer_index`.
- Award `round_score = 1` if correct, `0` if wrong.
- Add `round_score` to `session["score"]`.
- Increment `session["round"]` each time.
- When all 5 rounds are complete:
  - `final_score = session["score"]` (integer, 0–5)
  - Save to the `scores` table: `INSERT INTO scores (user_id, score) VALUES (?, ?)`
  - Store in `session["last_score"]` for the results page.
- Return JSON with keys: `correct` (bool), `round_score` (int), `total_score` (int), `round` (int), `done` (bool).

---

### Task 3 — Swatch Styling (CSS, `static/style.css`)

Write the CSS rule for `.swatch-btn`.

**Requirements:**
- 64×64px square with border-radius of 10px.
- 3px solid transparent border that turns white on hover.
- `cursor: pointer`.
- Smooth hover transition with `transform: scale(1.1)`.

Also complete the `transition` property on `.timer-bar` so it animates over 10 seconds.

---

### Task 4 (BONUS) — Distractor Algorithm (Python, `app.py`)

Replace the placeholder in `generate_distractors()`.

**Requirements:**
- Parse the target hex into R, G, B integers.
- Offset each channel randomly by ±15 to ±60 units.
- Clamp all values between 0 and 255.
- Ensure no distractor is within ±5 units on ALL three channels simultaneously.
- Return a list of 5 hex strings.

---

### Task 5 — Countdown Timer (JavaScript, `static/game.js`)

Complete the timer logic inside `loadRound()`.

**Requirements:**
- Reset `timerBar` width to `'100%'` immediately.
- Trigger the CSS transition by setting width to `'0%'` after ~50ms.
- Use `setInterval` to count down from 10 to 0, updating `countdownEl` each second.
- When the counter hits 0: hide the image and reveal the swatches.

---

### Task 6 — Submit Answer (JavaScript, `static/game.js`)

Complete `handleSwatchClick()` with a `fetch` POST request.

**Requirements:**
- POST to `/game/submit` with `Content-Type: application/json`.
- Body must contain `selected_index` and `answer_index`.
- On correct: show `✅ Correct! +1  |  Score: X / 5` in green.
- On wrong: show `❌ Wrong!  |  Score: X / 5` in red; highlight the correct swatch with a white border.
- Update the live score display: `runningScore.textContent = response.total_score + ' / 5'`.
- After 1500ms, call `loadRound()` to advance.

---

## Seeding Images

Before you can test the game, populate the `images` table.
Place cartoon PNG/JPG files in `static/images/` and run in your Flask shell:

```python
from app import db
db.execute("INSERT INTO images (filename, target_hex, label) VALUES (?, ?, ?)",
           'mickey.png', '#F4A460', 'Mickey Mouse skin tone')
```

Repeat for each image. `target_hex` must be a hex color visually present in that image.

---

## Grading Criteria (self-check)

| Criterion                       | Points |
|---------------------------------|--------|
| User auth (register/login)      | 20     |
| `/game/next` returns valid JSON | 20     |
| `/game/submit` saves score      | 20     |
| Timer works correctly           | 15     |
| Swatch click + feedback         | 15     |
| CSS styling (swatches + bar)    | 10     |
| Bonus: distractor algorithm     | +10    |
| **Total**                       | **100 (+10)** |
