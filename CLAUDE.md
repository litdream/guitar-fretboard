# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a CLI-based guitar fretboard visualization project written in Python. The goal is to create ASCII art representations of guitar fretboards that can be manipulated programmatically.

## Project Structure

- `lib/` - Core library containing classes and functions for fretboard manipulation
  - `lib/fret.py` - Main fretboard module with templates and manipulation functions
- `bin/` - (Planned) Executable CLI tools that will use the lib/ modules

## Architecture

### Fretboard Data Structure

The project uses a **list-of-lists** representation for fretboards:

1. **Templates** (`empty_fret_12`, `empty_fret_18`) are immutable string constants containing ASCII art
2. **Working fretboards** are created by converting templates to `list[list[char]]` using `create_fret()`
3. **Modifications** are made by directly indexing into the 2D list structure
4. **Display** is done by converting back to string using `fret_to_string()`

### Coordinate System

- **Strings**: Numbered 1-6 where:
  - 1 = high e string (top of display)
  - 6 = low E string (bottom of display)
- **Frets**: Numbered 0-12 (or 0-18) where:
  - 0 = open string (at the nut)
  - 1+ = fret positions
- **Grid Layout**: Each string occupies 2 rows (fret line + note position row)
- **Column spacing**: Nut is at column 3, each fret is 4 characters wide

### Key Functions (lib/fret.py)

- `create_fret(template)` - Convert template string to mutable list-of-lists
- `mark_note(fret, string_num, fret_num, marker='x')` - Mark a position on the fretboard
- `fret_to_string(fret)` - Convert list-of-lists back to displayable string

## Development Notes

- Templates are intentionally "wasted" (copied) rather than modified in place
- The `.gitignore` includes `lib/` as a distribution directory, but this project's `lib/` is source code and is tracked in git
- Emacs backup files (`~` and `#` files) are present in lib/ but gitignored
