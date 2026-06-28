/**
 * Match It — Game Logic
 * Handles the client-side game loop:
 *   1. Fetch round data from /game/next
 *   2. Display image for 10 seconds with countdown timer
 *   3. Hide image and show color swatches
 *   4. Submit answer to /game/submit
 *   5. Show feedback and load next round or redirect to /results
 */

document.addEventListener('DOMContentLoaded', () => {
    // DOM references
    const imageEl       = document.getElementById('game-image');
    const imageArea     = document.getElementById('image-area');
    const swatchesArea  = document.getElementById('swatches-area');
    const swatchesCont  = document.getElementById('swatches-container');
    const feedbackEl    = document.getElementById('feedback');
    const countdownEl   = document.getElementById('countdown');
    const timerBar      = document.getElementById('timer-bar');
    const roundNumEl    = document.getElementById('round-num');
    const loadingEl     = document.getElementById('loading');

    let currentAnswerIndex = null;  // correct swatch index for current round
    let countdownInterval  = null;  // holds the setInterval reference

    // -----------------------------------------------------------------------
    // loadRound: fetches /game/next and sets up the image + timer
    // -----------------------------------------------------------------------
    function loadRound() {
        // Hide swatches and show loading indicator
        swatchesArea.style.display = 'none';
        imageArea.style.display    = 'none';
        feedbackEl.textContent     = '';
        loadingEl.style.display    = 'block';

        fetch('/game/next')
            .then(res => res.json())
            .then(data => {
                loadingEl.style.display = 'none';

                // If all rounds are done, go to results page
                if (data.done) {
                    window.location.href = '/results';
                    return;
                }

                // Update round counter
                roundNumEl.textContent = data.round;

                // Store correct answer index for this round
                currentAnswerIndex = data.answer_index;

                // Set image source
                imageEl.src = data.image_url;
                imageArea.style.display = 'flex';

                // Build swatch buttons from data.swatches
                buildSwatches(data.swatches);

                /*
                TODO (TASK 5):
                -------------------------
                Start the 10-second countdown here.

                Steps:
                  1. Reset the timer bar width to '100%' immediately.
                  2. After a brief delay (e.g. 50ms) using setTimeout, set
                     timerBar.style.width = '0%'. The CSS transition you wrote
                     in style.css will animate this over 10 seconds.
                  3. Use setInterval to decrement a counter from 10 to 0 every
                     1000ms, updating countdownEl.textContent each tick.
                  4. When the counter reaches 0:
                     a. clearInterval(countdownInterval) to stop the ticker.
                     b. Hide the image: imageArea.style.display = 'none'
                     c. Show the swatches: swatchesArea.style.display = 'block'

                Hint: store your setInterval return value in `countdownInterval`
                so you can clear it if needed.
                */

                // PLACEHOLDER: immediately show swatches (no timer yet)
                // DELETE these two lines once you implement the timer above:
                imageArea.style.display = 'none';
                swatchesArea.style.display = 'block';
            })
            .catch(err => {
                loadingEl.textContent = 'Error loading round. Please refresh.';
                console.error(err);
            });
    }

    // -----------------------------------------------------------------------
    // buildSwatches: creates 6 colored button elements
    // -----------------------------------------------------------------------
    function buildSwatches(swatches) {
        swatchesCont.innerHTML = ''; // clear previous round's swatches
        swatches.forEach((hex, index) => {
            const btn = document.createElement('button');
            btn.classList.add('swatch-btn');
            btn.style.backgroundColor = hex;
            btn.dataset.index = index;

            btn.addEventListener('click', () => handleSwatchClick(index));
            swatchesCont.appendChild(btn);
        });
    }

    // -----------------------------------------------------------------------
    // handleSwatchClick: called when user picks a color
    // -----------------------------------------------------------------------
    function handleSwatchClick(selectedIndex) {
        // Disable all swatches to prevent double-clicking
        document.querySelectorAll('.swatch-btn').forEach(b => b.disabled = true);

        /*
        TODO (TASK 6):
        -------------------------
        Send the user's answer to the Flask backend using fetch().

        Steps:
          1. Use fetch('/game/submit', { method: 'POST', ... }) to POST JSON:
               { "selected_index": selectedIndex, "answer_index": currentAnswerIndex }
             Make sure to set the Content-Type header to 'application/json'.
             Use JSON.stringify() on the body.

          2. Parse the JSON response.

          3. If response.correct is true:
             - Set feedbackEl.textContent to '✅ Correct!'
             - Add class 'correct' to feedbackEl (remove 'wrong' if present)

          4. If response.correct is false:
             - Set feedbackEl.textContent to '❌ Wrong! The answer was swatch #(answer_index + 1)'
             - Add class 'wrong' to feedbackEl (remove 'correct' if present)
             - Optionally highlight the correct swatch button with a white border

          5. After a 1500ms delay (using setTimeout), call loadRound() again
             to move to the next round (or redirect to /results if done).

        Hint: fetch with POST + JSON body looks like:
            fetch('/game/submit', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ ... })
            })
        */

        // PLACEHOLDER: log the click (delete once you implement above)
        console.log('Swatch clicked:', selectedIndex, '| Correct:', currentAnswerIndex);
    }

    // -----------------------------------------------------------------------
    // Kick off the first round when the page loads
    // -----------------------------------------------------------------------
    loadRound();
});
