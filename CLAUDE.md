# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a CLI-based guitar fretboard visualization project written in Python. The project includes interactive learning games for practicing scales and triads, with ASCII art representations of guitar fretboards.

## Project Structure

- `lib/` - Core library containing classes and functions for fretboard manipulation
  - `lib/fret.py` - Main fretboard module with `Fretboard` class and templates
  - `lib/diatonic.py` - Diatonic scale generation (major/minor scales)
  - `lib/common_triad.py` - Triad chord generation and positioning
  - `lib/diatonic_test.py` - Unit tests for diatonic module
  - `lib/common_triad_test.py` - Unit tests for triad module
- `bin/` - Executable CLI games and tools
  - `bin/scale-speakout.py` - Interactive scale learning game
  - `bin/triad-1.py` - Interactive triad learning game

## Architecture

### Fretboard Data Structure

The project uses the `Fretboard` class (object-oriented approach):

1. **Templates** (`empty_fret_12`, `empty_fret_18`) are immutable string constants containing ASCII art
2. **Fretboard objects** are created with `Fretboard(num_frets)` which converts templates to `list[list[char]]`
3. **Modifications** are made using the `.mark(string_num, fret_num, marker)` method
4. **Display** is done by converting the object to string using `str(fretboard)` or `print(fretboard)`

### Coordinate System

- **Strings**: Numbered 1-6 where:
  - 1 = high e string (top of display)
  - 6 = low E string (bottom of display)
- **Frets**: Numbered 0-12 (or 0-18) where:
  - 0 = open string (at the nut, displays as 'o' when marked with 'x')
  - 1+ = fret positions
- **Grid Layout**: Each string occupies 2 rows (fret line + note position row)
- **Column spacing**: Nut is at column 3, each fret is 4 characters wide

### Standard Guitar Tuning

Standard tuning is defined in multiple modules (chromatic indices 0-11):
- String 1 (high e): E = 4
- String 2 (B): B = 11
- String 3 (G): G = 7
- String 4 (D): D = 2
- String 5 (A): A = 9
- String 6 (low E): E = 4

### Key Classes and Functions

#### lib/fret.py
- `Fretboard(num_frets=12)` - Create a fretboard object
- `.mark(string_num, fret_num, marker='x')` - Mark a position on the fretboard (supports method chaining)
- `__str__()` - Convert fretboard to displayable string

#### lib/diatonic.py
- `Diatonic(keyname)` - Create a diatonic scale (e.g., "C", "Amin", "F#", "Dmin")
- `.scale` - List of 7 note names in the scale
- `.use_flats` - Boolean indicating if scale uses flats or sharps
- `ENHARMONIC_MAP` - Dictionary mapping note names to chromatic indices (0-11)

#### lib/common_triad.py
- `Triad(root, is_major=True)` - Create a triad chord object
- `.find_position(inversion=0, start_fret=0, max_fret=12)` - Find fretboard position for triad on strings 2, 3, 4
- `.get_note_names(inversion=0)` - Get the three notes in the triad for a given inversion
- `.format_answer(inversion=0)` - Format the answer string (e.g., "c e g")
- `parse_triad_spec(spec)` - Parse strings like "C major" or "A minor"

### Interactive Games

Both games follow similar patterns:

#### bin/scale-speakout.py
- Interactive CLI game for learning major and minor scales
- Tests knowledge of scale notes in order (7 or 8 notes)
- Displays scales on 18-fret board with 3 notes per string
- Features:
  - Weighted random selection (simpler keys appear more often)
  - Color-coded feedback (green for correct, red for wrong)
  - Root notes displayed as 'R' instead of 'x'
  - Score tracking
  - Accepts 'quit' or 'exit' to exit

#### bin/triad-1.py
- Interactive CLI game for learning major and minor triads
- Tests knowledge of triad notes in different inversions
- Displays triads on 12-fret board on strings 2, 3, 4 (electric guitar voicing)
- Features:
  - Three inversions: no-inversion, 1st-inversion, 2nd-inversion
  - Color-coded feedback (green for correct, red for wrong)
  - Root notes displayed as 'R' instead of 'x'
  - Score tracking
  - Accepts 'quit' or 'exit' to exit
  - **Accepts enharmonic equivalents** (Eb and D# are considered the same)

### Display Conventions

- **'R'**: Root note of the scale/triad
- **'x'**: Other scale/triad notes
- **'o'**: Open string (when marking fret 0 with 'x')
- **Colors** (ANSI codes):
  - Green: Correct notes (always shown, whether user answer is correct or incorrect)
  - Red: Wrong notes (only shown when user makes errors)

## Testing

- Run tests with: `uv run pytest`
- Test files are located in `lib/` with `_test.py` suffix
- Comprehensive test coverage for diatonic and triad modules

## Development Notes

- Templates are intentionally "wasted" (copied) rather than modified in place
- The `.gitignore` includes `lib/` as a distribution directory, but this project's `lib/` is source code and is tracked in git
- Emacs backup files (`~` and `#` files) are present in lib/ but gitignored
- The project uses `uv` for dependency management and running tests
- All games use ANSI color codes for terminal output
- Games are designed to be educational tools for learning guitar theory

### Enharmonic Equivalents

- **Scale game (scale-speakout.py)**: Requires exact note names as they appear in the scale (e.g., in F major, you must type "Bb" not "A#")
- **Triad game (triad-1.py)**: Accepts enharmonic equivalents - users can answer with either sharps or flats (e.g., "Eb" and "D#" are both accepted)
- This design choice reflects that:
  - Scales have specific note spellings based on music theory (e.g., C major uses F#, not Gb)
  - Triads are more flexible in practice - guitarists can think of intervals using either notation
- Implementation: Triad answer checking compares chromatic indices (0-11) rather than string matching
