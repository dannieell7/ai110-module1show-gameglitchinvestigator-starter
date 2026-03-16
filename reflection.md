# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
  - The game looked like a normal webapp the first time i ran it.
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").
  - There were no hints all together
  - The counter did not decrement based on my attempts (e.g. i made 2 attempts before the counter went down by 1)
  - The thing that says go higher is completely wrong, it told me to go higher even when the number was           significantly lower than my guesses.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
  - I used Claude Code (Anthropic) running directly in my terminal as an agentic AI assistant. It could read files, edit code, run tests, and explain its reasoning at each step — similar to Copilot Agent mode but through the CLI.

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
  - **Correct suggestion — hint direction bug:** Claude Code read `check_guess` and immediately flagged that the hint messages were swapped: when `guess > secret` the code returned `"📈 Go HIGHER!"` and when `guess < secret` it returned `"📉 Go LOWER!"` — both backwards. Claude suggested swapping the messages so `guess > secret` returns `"Go LOWER!"` and `guess < secret` returns `"Go HIGHER!"`. I verified this by running the app with `streamlit run app.py`, guessing a number I knew was too high (e.g., guessing 90 when the secret debug panel showed 42), and confirming the hint now correctly said "Go LOWER!" instead of the old misleading "Go HIGHER!".

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
  - **Misleading suggestion — initial mock for pytest:** When I asked Claude to generate pytest cases, its first attempt mocked the `streamlit` module with a plain `MagicMock()` and then tried to import `app.py` directly. This failed because `app.py` runs module-level Streamlit code (like `st.sidebar.selectbox()`) that the generic mock couldn't handle — it returned a `MagicMock` object as the difficulty value, causing a `KeyError` when that object was used as a dictionary key. Claude's second attempt set `selectbox.return_value = "Normal"` but then hit another error with `session_state`. The real fix was to stop importing `app.py` in tests entirely and instead implement the pure logic functions in `logic_utils.py`, which has no Streamlit dependency. I verified this worked by running `python3 -m pytest tests/test_game_logic.py -v` and seeing all 9 tests pass cleanly.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
  - For each bug I used two layers of verification: first I ran `streamlit run app.py` and manually tested the exact scenario that triggered the bug (e.g., submitting a guess higher than the secret to check hint direction, and watching the "Attempts left" counter on the first guess to check the decrement). Second, I ran `python3 -m pytest tests/test_game_logic.py -v` and confirmed all 9 automated tests passed. A bug was only considered fixed when both checks agreed.

- Describe at least one test you ran (manual or using pytest) and what it showed you about your code.
  - The most revealing pytest test was `test_string_comparison_bug_with_single_digit_vs_two_digit`. It called `check_guess(9, 10)` — a case where the old code would cast the secret to the string `"10"` on even attempts and then compare `"9" > "10"` lexicographically, which evaluates to `True` in Python because `"9"` sorts after `"1"`. That made the function return `"Too High"` even though 9 is less than 10. The test asserted `outcome == "Too Low"` and confirmed that after removing the type-juggling and always passing an integer secret, the comparison works correctly every time.

- Did AI help you design or understand any tests? How?
  - Yes. I described the three bugs to Claude Code and asked it to generate pytest cases targeting each one. Claude structured the tests in three clearly labeled groups (one per bug), wrote docstrings that explained what pre-fix behavior each test was catching, and chose edge cases I hadn't thought of — like the single-digit vs two-digit lexicographic comparison for Bug 3. Claude also diagnosed why the first import-based approach failed and proposed the cleaner solution of moving logic into `logic_utils.py` so tests had no Streamlit dependency at all.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
