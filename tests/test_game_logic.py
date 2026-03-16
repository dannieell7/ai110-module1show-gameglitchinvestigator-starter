import sys
import os

# Allow imports from the project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from logic_utils import check_guess, parse_guess, update_score


# ---------------------------------------------------------------------------
# Bug 1 — Hint direction was backwards in check_guess
# Before fix: guess > secret returned "Go HIGHER!" (wrong)
#             guess < secret returned "Go LOWER!"  (wrong)
# ---------------------------------------------------------------------------

def test_hint_says_go_lower_when_guess_is_too_high():
    """Guess above secret must tell the player to go LOWER, not higher."""
    outcome, message = check_guess(80, 50)
    assert outcome == "Too High"
    assert "LOWER" in message, f"Expected 'LOWER' in hint, got: '{message}'"

def test_hint_says_go_higher_when_guess_is_too_low():
    """Guess below secret must tell the player to go HIGHER, not lower."""
    outcome, message = check_guess(20, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message, f"Expected 'HIGHER' in hint, got: '{message}'"

def test_hint_direction_not_inverted_for_close_guess():
    """Even a guess just 1 off must return the correct direction."""
    outcome_high, msg_high = check_guess(51, 50)
    assert outcome_high == "Too High"
    assert "LOWER" in msg_high

    outcome_low, msg_low = check_guess(49, 50)
    assert outcome_low == "Too Low"
    assert "HIGHER" in msg_low


# ---------------------------------------------------------------------------
# Bug 2 — Counter did not decrement correctly because attempts was
#          initialised to 1 instead of 0, causing the first real guess
#          to arrive at update_score as attempt_number=2 instead of 1,
#          shifting all score calculations by one slot.
# ---------------------------------------------------------------------------

def test_score_on_first_attempt_starts_from_one_not_two():
    """
    With the fix, the first guess is attempt_number=1.
    Before the fix attempts started at 1 so the increment made the first
    guess arrive as attempt_number=2, shifting all score calculations.
    Win on attempt 1 → points = 100 - 10*(1+1) = 80.
    """
    score_after = update_score(0, "Win", attempt_number=1)
    assert score_after == 80, f"Expected 80, got {score_after}"

def test_score_win_on_attempt_two():
    """Win on attempt 2 → points = 100 - 10*(2+1) = 70."""
    score_after = update_score(0, "Win", attempt_number=2)
    assert score_after == 70, f"Expected 70, got {score_after}"

def test_attempts_counter_floor_keeps_minimum_points():
    """Win very late should award at least 10 points (floor check)."""
    score_after = update_score(0, "Win", attempt_number=20)
    assert score_after >= 10


# ---------------------------------------------------------------------------
# Bug 3 — Type-juggling converted secret to str on even attempts, breaking
#          check_guess comparisons (int vs str raises TypeError in Python 3,
#          falling through to a broken lexicographic string-comparison path).
#          After the fix, secret is always an int.
# ---------------------------------------------------------------------------

def test_integer_secret_returns_correct_outcome():
    """check_guess with integer secret must always return the right outcome."""
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"

def test_string_comparison_bug_with_single_digit_vs_two_digit():
    """
    Demonstrates why passing str(secret) was a bug:
    lexicographic '9' > '10' is True, so check_guess(9, 10) would have
    wrongly returned 'Too High' via the old string path.
    With integer secrets it correctly returns 'Too Low'.
    """
    outcome, _ = check_guess(9, 10)
    assert outcome == "Too Low", (
        f"Expected 'Too Low' (9 < 10), got '{outcome}'. "
        "This catches the old string-comparison bug where '9' > '10' lexicographically."
    )

def test_correct_guess_still_wins():
    """Sanity-check: an exact match always returns Win."""
    outcome, message = check_guess(42, 42)
    assert outcome == "Win"
    assert "Correct" in message
