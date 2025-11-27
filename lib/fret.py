import os

empty_fret_12 = """\
e ||---+---+---+---+---+---+---+---+---+---+---+---+--
  ||   |   |   |   |   |   |   |   |   |   |   |   |
B ||---|---|---|---|---|---|---|---|---|---|---|---|--
  ||   |   |   |   |   |   |   |   |   |   |   | . |
G ||---|---|---|---|---|---|---|---|---|---|---|---|--
  ||   |   | . |   | . |   | . |   | . |   |   |   |
D ||---|---|---|---|---|---|---|---|---|---|---|---|--
  ||   |   |   |   |   |   |   |   |   |   |   | . |
A ||---|---|---|---|---|---|---|---|---|---|---|---|--
  ||   |   |   |   |   |   |   |   |   |   |   |   |
E ||---+---+---+---+---+---+---+---+---+---+---+---+--

"""

empty_fret_18 = """\
e ||---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+--
  ||   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
B ||---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|--
  ||   |   |   |   |   |   |   |   |   |   |   | . |   |   |   |   |   |   |
G ||---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|--
  ||   |   | . |   | . |   | . |   | . |   |   |   |   |   | . |   | . |   | .
D ||---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|--
  ||   |   |   |   |   |   |   |   |   |   |   | . |   |   |   |   |   |   |
A ||---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|--
  ||   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
E ||---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+--

"""


class Fretboard:
    """A guitar fretboard representation that can be marked and displayed."""

    def __init__(self, num_frets=12):
        """Create a fretboard with specified number of frets.

        Args:
            num_frets: Number of frets (12 or 18, default 12)
        """
        if num_frets == 12:
            template = empty_fret_12
        elif num_frets == 18:
            template = empty_fret_18
        else:
            raise ValueError("num_frets must be 12 or 18")

        self.grid = [list(line) for line in template.split('\n')]
        self.num_frets = num_frets

    def mark(self, string_num, fret_num, marker='x'):
        """Mark a position on the fretboard with a character.

        Args:
            string_num: String number (1=high e, 2=B, 3=G, 4=D, 5=A, 6=low E)
            fret_num: Fret number (0=open, 1=first fret, etc.)
            marker: Character to place at the position (default 'x')

        Returns:
            self (for method chaining)

        Example:
            fret = Fretboard(12)
            fret.mark(6, 1, 'x')  # Mark F on low E string, 1st fret
            print(fret)
        """
        # Calculate row index - each string has 2 rows (fret line + note row)
        row = (string_num - 1) * 2

        # Calculate column index - each fret is 4 chars wide
        if fret_num == 0:
            col = 2  # Open string position (at the nut)
        else:
            col = 1 + (fret_num * 4)  # Center of each fret

        # Check for Special case for Open String with 'x'
        #   Otherwise, simply locate and print.
        #
        if fret_num == 0 and marker == 'x':
            self.grid[row][col] = 'o'
        else:
            self.grid[row][col] = marker
        
        return self

    def __str__(self):
        """Return string representation for printing.

        Returns:
            String representation of the fretboard
        """
        return '\n'.join(''.join(line) for line in self.grid)


