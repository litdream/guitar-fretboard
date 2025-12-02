#!/usr/bin/env python3
"""Scale Speak-Out Game

A CLI game that tests your knowledge of major and minor scales.
The game presents a scale (following the circle of fifths) with its
sharps/flats, and you must type out the notes in order.

Example:
  Question: G major (1 sharp: F)
  Answer: g a b c d e f# (or g a b c d e f# g)

Usage:
  python bin/scale-speakout.py
"""

import sys
import random
from pathlib import Path

# Add lib directory to path so we can import diatonic
lib_path = Path(__file__).parent.parent / 'lib'
sys.path.insert(0, str(lib_path))

from diatonic import Diatonic, ENHARMONIC_MAP
from fret import Fretboard

# ANSI color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'

# Standard guitar tuning (string number: open note index in chromatic scale)
# String 1 (high e) = E = 4, String 2 (B) = B = 11, etc.
GUITAR_TUNING = {
    1: 4,   # high e (E)
    2: 11,  # B
    3: 7,   # G
    4: 2,   # D
    5: 9,   # A
    6: 4,   # low E
}

# Circle of Fifths - Major keys (sharps) - up to 6 sharps
MAJOR_SHARP_KEYS = [
    ('C', 0, []),
    ('G', 1, ['F']),
    ('D', 2, ['F', 'C']),
    ('A', 3, ['F', 'C', 'G']),
    ('E', 4, ['F', 'C', 'G', 'D']),
    ('B', 5, ['F', 'C', 'G', 'D', 'A']),
    ('F#', 6, ['F', 'C', 'G', 'D', 'A', 'E']),
]

# Circle of Fifths - Major keys (flats) - up to 6 flats
MAJOR_FLAT_KEYS = [
    ('F', 1, ['B']),
    ('Bb', 2, ['B', 'E']),
    ('Eb', 3, ['B', 'E', 'A']),
    ('Ab', 4, ['B', 'E', 'A', 'D']),
    ('Db', 5, ['B', 'E', 'A', 'D', 'G']),
    ('Gb', 6, ['B', 'E', 'A', 'D', 'G', 'C']),
]

# Circle of Fifths - Minor keys (sharps) - up to 6 sharps
MINOR_SHARP_KEYS = [
    ('Amin', 0, []),
    ('Emin', 1, ['F']),
    ('Bmin', 2, ['F', 'C']),
    ('F#min', 3, ['F', 'C', 'G']),
    ('C#min', 4, ['F', 'C', 'G', 'D']),
    ('G#min', 5, ['F', 'C', 'G', 'D', 'A']),
    ('D#min', 6, ['F', 'C', 'G', 'D', 'A', 'E']),
]

# Circle of Fifths - Minor keys (flats) - up to 6 flats
MINOR_FLAT_KEYS = [
    ('Dmin', 1, ['B']),
    ('Gmin', 2, ['B', 'E']),
    ('Cmin', 3, ['B', 'E', 'A']),
    ('Fmin', 4, ['B', 'E', 'A', 'D']),
    ('Bbmin', 5, ['B', 'E', 'A', 'D', 'G']),
    ('Ebmin', 6, ['B', 'E', 'A', 'D', 'G', 'C']),
]

# Combine all keys
ALL_KEYS = MAJOR_SHARP_KEYS + MAJOR_FLAT_KEYS + MINOR_SHARP_KEYS + MINOR_FLAT_KEYS


def create_weighted_key_pool():
    """Create a weighted pool of keys where simpler keys appear more frequently.

    Keys with 0 sharps/flats appear 5 times
    Keys with 1 sharp/flat appear 4 times
    Keys with 2 sharps/flats appear 4 times
    Keys with 3 sharps/flats appear 3 times
    Keys with 4 sharps/flats appear 2 times
    Keys with 5 sharps/flats appear 2 times
    Keys with 6 sharps/flats appear 1 time

    Returns:
        List of keys with weighted duplicates for random selection
    """
    weighted_pool = []

    for key_name, accidental_count, accidental_notes in ALL_KEYS:
        # Determine weight based on number of accidentals
        if accidental_count == 0:
            weight = 5
        elif accidental_count == 1:
            weight = 4
        elif accidental_count == 2:
            weight = 4
        elif accidental_count == 3:
            weight = 3
        elif accidental_count == 4:
            weight = 2
        elif accidental_count == 5:
            weight = 2
        else:  # 6 sharps/flats
            weight = 1

        # Add this key to the pool 'weight' times
        for _ in range(weight):
            weighted_pool.append((key_name, accidental_count, accidental_notes))

    return weighted_pool


def format_accidentals(count, notes, use_flats):
    """Format the accidentals description for display.

    Args:
        count: Number of sharps or flats
        notes: List of note names that are sharp/flat
        use_flats: True if using flats, False if using sharps

    Returns:
        Formatted string like "1 sharp: F" or "3 flats: B E A"
    """
    if count == 0:
        return "no sharps or flats"

    accidental_type = "flat" if use_flats else "sharp"
    if count > 1:
        accidental_type += "s"

    notes_str = " ".join(notes)
    return f"{count} {accidental_type}: {notes_str}"


def normalize_answer(answer):
    """Normalize user answer by converting to lowercase and splitting into notes.

    Args:
        answer: User's input string

    Returns:
        List of normalized note names (lowercase)
    """
    return answer.lower().strip().split()


def check_answer(user_notes, correct_scale):
    """Check if the user's answer matches the correct scale.

    Args:
        user_notes: List of user-provided note names (lowercase)
        correct_scale: List of correct note names from Diatonic

    Returns:
        True if answer is correct, False otherwise
    """
    # Convert correct scale to lowercase for comparison
    correct_lower = [note.lower() for note in correct_scale]

    # User can provide 7 notes or 8 notes (with octave)
    if len(user_notes) == 7:
        return user_notes == correct_lower
    elif len(user_notes) == 8:
        # Last note should be the same as the first (octave)
        return (user_notes[:7] == correct_lower and
                user_notes[7] == user_notes[0])
    else:
        return False


def display_scale_on_fretboard(scale, user_notes=None, start_note_offset=0):
    """Display the scale on a guitar fretboard with 3 notes per string in order.

    The scale is displayed sequentially across strings, only moving up the fretboard.
    If user_notes provided, mark user's notes first, then overwrite correct positions
    with green (leaving wrong notes in red).

    Args:
        scale: Diatonic scale object with .scale attribute
        user_notes: List of user-provided note names (lowercase), or None
        start_note_offset: Index of the scale note to start the pattern from (0-6)

    Returns:
        String representation of the fretboard with scale notes marked,
        with colors if user_notes is provided
    """
    fretboard = Fretboard(18)

    user_positions = []
    correct_positions = []

    # Get the root note index for marking with 'R'
    root_note = scale.scale[0]
    root_index = ENHARMONIC_MAP[root_note]

    # If user notes provided, first mark user's answer on the fretboard
    if user_notes is not None and len(user_notes) >= 7:
        note_position = start_note_offset
        min_fret = 0

        # For each string (6 to 1), mark 3 consecutive notes from user's answer
        for string_num in range(6, 0, -1):
            open_note_index = GUITAR_TUNING[string_num]
            notes_marked = 0
            first_note_fret = None

            # Search through frets starting from min_fret for the next 3 user notes
            for fret_num in range(min_fret, 19):
                # Calculate what note is at this fret
                note_index = (open_note_index + fret_num) % 12

                # Get the chromatic index of the current user note we're looking for
                user_note = user_notes[note_position % 7]
                # Handle both sharp and flat notation
                user_note_normalized = user_note.capitalize()
                if user_note_normalized not in ENHARMONIC_MAP:
                    # Try adding # or b if it's a two-character note
                    if len(user_note) > 1:
                        user_note_normalized = user_note[0].upper() + user_note[1]

                if user_note_normalized in ENHARMONIC_MAP:
                    target_index = ENHARMONIC_MAP[user_note_normalized]

                    # If this fret matches the current user note we're looking for
                    if note_index == target_index:
                        # Mark with 'R' if it's the root note, otherwise 'x'
                        marker = 'R' if note_index == root_index else 'x'
                        fretboard.mark(string_num, fret_num, marker)
                        user_positions.append((string_num, fret_num))
                        notes_marked += 1

                        # Track the first note's fret on this string
                        if first_note_fret is None:
                            first_note_fret = fret_num

                        note_position += 1

                        # Stop after marking 3 notes on this string
                        if notes_marked >= 3:
                            break

            # Update min_fret to the position of the first note on this string
            if first_note_fret is not None:
                min_fret = first_note_fret

    # Now mark the correct answer (may overwrite some user positions)
    scale_position = start_note_offset
    min_fret = 0  # Minimum fret position (updated as we progress)

    # For each string (6 to 1), mark 3 consecutive notes from the scale
    for string_num in range(6, 0, -1):
        open_note_index = GUITAR_TUNING[string_num]
        notes_marked = 0
        first_note_fret = None

        # Search through frets starting from min_fret for the next 3 scale notes
        for fret_num in range(min_fret, 19):
            # Calculate what note is at this fret
            note_index = (open_note_index + fret_num) % 12

            # Get the chromatic index of the current scale note we're looking for
            target_note = scale.scale[scale_position % 7]
            target_index = ENHARMONIC_MAP[target_note]

            # If this fret matches the current scale note we're looking for
            if note_index == target_index:
                # Mark with 'R' if it's the root note, otherwise 'x'
                marker = 'R' if note_index == root_index else 'x'
                fretboard.mark(string_num, fret_num, marker)
                correct_positions.append((string_num, fret_num))
                notes_marked += 1

                # Track the first note's fret on this string
                if first_note_fret is None:
                    first_note_fret = fret_num

                scale_position += 1

                # Stop after marking 3 notes on this string
                if notes_marked >= 3:
                    break

        # Update min_fret to the position of the first note on this string
        if first_note_fret is not None:
            min_fret = first_note_fret

    # Apply colors to the fretboard string output
    fretboard_str = str(fretboard)

    # Always apply colors
    if user_notes is not None:
        # Find positions that are only in user's answer (wrong notes)
        wrong_positions = [pos for pos in user_positions if pos not in correct_positions]
        # Color wrong notes red, correct notes green
        fretboard_str = colorize_fretboard(fretboard_str, correct_positions, wrong_positions)
    else:
        # No user notes - show correct positions in green
        fretboard_str = colorize_fretboard(fretboard_str, correct_positions, [])

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

    # Create a list to store positions that need coloring for each line
    # Format: {row: [(col, color), ...]}
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

    # Apply colors to each line by rebuilding them character by character
    for row, positions in color_map.items():
        if row >= len(lines):
            continue

        line = lines[row]
        # Sort positions in reverse order to apply colors from right to left
        # This prevents index shifting issues
        positions_sorted = sorted(positions, key=lambda x: x[0], reverse=True)

        for col, color in positions_sorted:
            if col < len(line):
                char = line[col]
                line = line[:col] + color + char + Colors.RESET + line[col+1:]

        lines[row] = line

    return '\n'.join(lines)


def print_final_score(score, total):
    """Display the final score and accuracy."""
    print()
    print("=" * 60)
    print(f"Final Score: {score}/{total}")
    if total > 0:
        percentage = (score / total) * 100
        print(f"Accuracy: {percentage:.1f}%")
    print("Thanks for playing!")
    print("=" * 60)


def play_game():
    """Main game loop."""
    print("=" * 60)
    print("Welcome to Scale Speak-Out!")
    print("=" * 60)
    print()
    print("Enter the notes of the scale in order.")
    print("You can enter 7 notes or 8 notes (with octave).")
    print("Example: g a b c d e f# or g a b c d e f# g")
    print()
    print("Type 'quit' or 'exit' to exit the game.")
    print("=" * 60)
    print()

    score = 0
    total = 0

    # Create weighted pool once at the start
    weighted_pool = create_weighted_key_pool()

    while True:
        # Select a random key from the weighted pool
        key_name, accidental_count, accidental_notes = random.choice(weighted_pool)

        # Create the scale
        scale = Diatonic(key_name)

        # Determine if using flats or sharps
        use_flats = scale.use_flats

        # Format the question
        accidentals_str = format_accidentals(accidental_count, accidental_notes, use_flats)

        # Display the question
        print(f"Question: {key_name} ({accidentals_str})")
        print()

        # Get user input
        user_input = input("Your answer: ").strip()

        # Check for quit or exit
        if user_input.lower() in ['quit', 'exit']:
            print_final_score(score, total)
            break

        # Normalize and check the answer
        user_notes = normalize_answer(user_input)
        correct = check_answer(user_notes, scale.scale)

        total += 1

        if correct:
            score += 1
            print("✓ Correct!")
        else:
            print("✗ Incorrect!")
            print(f"  Correct answer: {' '.join(note.lower() for note in scale.scale)}")

        print(f"  Score: {score}/{total}")
        print()

        # Loop for showing fretboard and handling left/right shifts
        start_note_offset = 0
        while True:
            fretboard_display = display_scale_on_fretboard(scale, user_notes, start_note_offset)
            print(fretboard_display)
            print()
            print("Type 'left' or 'right' to shift pattern, Enter to continue, or 'quit' to exit.")
            command = input("> ").strip().lower()

            if command == 'left':
                start_note_offset = (start_note_offset - 1 + 7) % 7
            elif command == 'right':
                start_note_offset = (start_note_offset + 1) % 7
            elif command in ['quit', 'exit']:
                print_final_score(score, total)
                return
            else:
                break

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
