#!/usr/bin/env python3
"""Triad Game

A CLI game that tests your knowledge of major and minor triads.
The game asks you to identify the notes of a triad in a specific inversion
(e.g., "C major, no-inversion" = "c e g", "A minor, 1st-inversion" = "c e a").

After answering, the fretboard is displayed showing where the triad is played
on strings 2, 3, 4.

Usage:
  python bin/triad-1.py
"""

import sys
import random
from pathlib import Path

# Add lib directory to path so we can import modules
lib_path = Path(__file__).parent.parent / 'lib'
sys.path.insert(0, str(lib_path))

from common_triad import Triad, parse_triad_spec
from fret import Fretboard

# ANSI color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'

# Common triads to practice
COMMON_TRIADS = [
    'C major', 'D major', 'E major', 'F major', 'G major', 'A major', 'B major',
    'A minor', 'B minor', 'C minor', 'D minor', 'E minor', 'F minor', 'G minor',
]

# Inversions: 0 = no-inversion, 1 = 1st-inversion, 2 = 2nd-inversion
INVERSIONS = [0, 1, 2]


def normalize_answer(answer):
    """Normalize user answer by converting to lowercase and splitting into notes.

    Args:
        answer: User's input string

    Returns:
        List of normalized note names (lowercase)
    """
    return answer.lower().strip().split()


def check_answer(user_notes, correct_notes):
    """Check if the user's answer matches the correct notes.

    Args:
        user_notes: List of user-provided note names (lowercase)
        correct_notes: List of correct note names (lowercase)

    Returns:
        True if answer is correct, False otherwise
    """
    return user_notes == correct_notes


def display_triad_on_fretboard(position, user_position=None):
    """Display the triad on a guitar fretboard.

    Args:
        position: List of (string_num, fret_num) tuples for correct positions
        user_position: List of (string_num, fret_num) tuples for user's answer, or None

    Returns:
        String representation of the fretboard with triad notes marked
    """
    fretboard = Fretboard(12)

    # Mark all positions (both user's and correct)
    all_positions = set()

    if user_position is not None:
        for string_num, fret_num in user_position:
            fretboard.mark(string_num, fret_num, 'x')
            all_positions.add((string_num, fret_num))

    for string_num, fret_num in position:
        fretboard.mark(string_num, fret_num, 'x')
        all_positions.add((string_num, fret_num))

    fretboard_str = str(fretboard)

    # Add colors if user position was provided
    if user_position is not None:
        # Find wrong positions (in user_position but not in position)
        wrong_positions = [pos for pos in user_position if pos not in position]
        fretboard_str = colorize_fretboard(fretboard_str, position, wrong_positions)
    else:
        # No user position - just show correct positions without colors
        pass

    return fretboard_str


def colorize_fretboard(fretboard_str, correct_positions, wrong_positions):
    """Add ANSI color codes to fretboard string.

    Args:
        fretboard_str: String representation of fretboard
        correct_positions: List of (string_num, fret_num) tuples for correct notes
        wrong_positions: List of (string_num, fret_num) tuples for wrong notes

    Returns:
        Colored fretboard string
    """
    lines = list(fretboard_str.split('\n'))

    # Create a map of positions that need coloring
    color_map = {}

    for string_num, fret_num in correct_positions:
        row = (string_num - 1) * 2
        if fret_num == 0:
            col = 2
        else:
            col = 1 + (fret_num * 4)

        if row not in color_map:
            color_map[row] = []
        color_map[row].append((col, Colors.GREEN))

    for string_num, fret_num in wrong_positions:
        row = (string_num - 1) * 2
        if fret_num == 0:
            col = 2
        else:
            col = 1 + (fret_num * 4)

        if row not in color_map:
            color_map[row] = []
        color_map[row].append((col, Colors.RED))

    # Apply colors to each line
    for row, positions in color_map.items():
        if row >= len(lines):
            continue

        line = lines[row]
        # Sort positions in reverse order to prevent index shifting
        positions_sorted = sorted(positions, key=lambda x: x[0], reverse=True)

        for col, color in positions_sorted:
            if col < len(line):
                char = line[col]
                line = line[:col] + color + char + Colors.RESET + line[col+1:]

        lines[row] = line

    return '\n'.join(lines)


def parse_user_position(user_notes, inversion, triad):
    """Parse user's note answer into fretboard positions on strings 4, 3, 2.

    Args:
        user_notes: List of user-provided note names (lowercase)
        inversion: The inversion being tested (0, 1, or 2)
        triad: The Triad object for this question

    Returns:
        List of (string_num, fret_num) tuples for user's notes, or None if cannot parse
    """
    from diatonic import ENHARMONIC_MAP
    from common_triad import GUITAR_TUNING

    # We need exactly 3 notes
    if len(user_notes) != 3:
        return None

    positions = []
    target_strings = [4, 3, 2]  # D, G, B strings

    # Get the correct position to determine the fret range
    correct_position = triad.find_position(inversion)
    if not correct_position:
        return None

    # Determine the fret range to search (around where the correct answer is)
    min_fret = min(fret for _, fret in correct_position)
    max_fret = max(fret for _, fret in correct_position) + 5
    min_fret = max(0, min_fret - 3)

    # For each of the three user notes, find it on the corresponding string
    for i, user_note in enumerate(user_notes):
        string_num = target_strings[i]

        # Normalize the user note name
        user_note_normalized = user_note.capitalize()
        if len(user_note) > 1 and user_note[1] in ['#', 'b']:
            user_note_normalized = user_note[0].upper() + user_note[1]

        # Get the chromatic index for this note
        if user_note_normalized not in ENHARMONIC_MAP:
            return None

        target_index = ENHARMONIC_MAP[user_note_normalized]

        # Find this note on the target string within the fret range
        open_note = GUITAR_TUNING[string_num]
        found = False

        for fret_num in range(min_fret, min(max_fret + 1, 13)):
            note_at_fret = (open_note + fret_num) % 12
            if note_at_fret == target_index:
                positions.append((string_num, fret_num))
                found = True
                break

        if not found:
            # Try the whole range if not found in the limited range
            for fret_num in range(0, 13):
                note_at_fret = (open_note + fret_num) % 12
                if note_at_fret == target_index:
                    positions.append((string_num, fret_num))
                    found = True
                    break

        if not found:
            return None

    return positions if len(positions) == 3 else None


def play_game():
    """Main game loop."""
    print("=" * 60)
    print("Welcome to Triad Game!")
    print("=" * 60)
    print()
    print("Identify the notes of the triad in the specified inversion.")
    print("Enter the notes from lowest to highest string (4, 3, 2).")
    print("Example: 'c e g' or 'c e a'")
    print()
    print("Type 'quit' or 'exit' to exit the game.")
    print("=" * 60)
    print()

    score = 0
    total = 0

    while True:
        # Select a random triad and inversion
        triad_spec = random.choice(COMMON_TRIADS)
        inversion = random.choice(INVERSIONS)

        # Create the triad object
        root, is_major = parse_triad_spec(triad_spec)
        triad = Triad(root, is_major)

        # Get the correct answer
        correct_notes_str = triad.format_answer(inversion)
        correct_notes = correct_notes_str.split()

        # Get inversion name
        inversion_name = triad.get_inversion_name(inversion)

        # Display the question
        print(f"Question: {triad_spec}, {inversion_name}")
        print()

        # Get user input
        user_input = input("Your answer: ").strip()

        # Check for quit or exit
        if user_input.lower() in ['quit', 'exit']:
            print()
            print("=" * 60)
            print(f"Final Score: {score}/{total}")
            if total > 0:
                percentage = (score / total) * 100
                print(f"Accuracy: {percentage:.1f}%")
            print("Thanks for playing!")
            print("=" * 60)
            break

        # Normalize and check the answer
        user_notes = normalize_answer(user_input)
        correct = check_answer(user_notes, correct_notes)

        total += 1

        if correct:
            score += 1
            print(f"{Colors.GREEN}✓ Correct!{Colors.RESET}")
        else:
            print(f"{Colors.RED}✗ Incorrect!{Colors.RESET}")
            print(f"  Correct answer: {correct_notes_str}")

        print(f"  Score: {score}/{total}")
        print()

        # Find and display the fretboard position
        position = triad.find_position(inversion)
        if position:
            # Parse user position to show their wrong notes in red
            user_position = parse_user_position(user_notes, inversion, triad) if not correct else None
            fretboard_display = display_triad_on_fretboard(position, user_position)
            print(fretboard_display)
        else:
            print("(No position found on fretboard for this triad)")

        print()
        print("-" * 60)
        print()


def main():
    """Entry point for the game."""
    try:
        play_game()
    except KeyboardInterrupt:
        print()
        print()
        print("Game interrupted. Goodbye!")
        sys.exit(0)


if __name__ == "__main__":
    main()
