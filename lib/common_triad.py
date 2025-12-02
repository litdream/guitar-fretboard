"""Common Triads are electric guitar triads using strings 2, 3, 4.

There are 3 shapes: root position (no inversion), 1st inversion, 2nd inversion.

For major triads (e.g., C major = C E G):
- Root position: root on string 4, 3rd on string 3, 5th on string 2
- 1st inversion: 3rd on string 4, 5th on string 3, root on string 2
- 2nd inversion: 5th on string 4, root on string 3, 3rd on string 2

For minor triads (e.g., A minor = A C E):
- Root position: root on string 4, b3 on string 3, 5th on string 2
- 1st inversion: b3 on string 4, 5th on string 3, root on string 2
- 2nd inversion: 5th on string 4, root on string 3, b3 on string 2
"""

from diatonic import ENHARMONIC_MAP

# Major triad intervals from root: 0, 4, 7 semitones
MAJOR_INTERVALS = [0, 4, 7]

# Minor triad intervals from root: 0, 3, 7 semitones
MINOR_INTERVALS = [0, 3, 7]

# Standard guitar tuning (string number: open note index in chromatic scale)
GUITAR_TUNING = {
    1: 4,   # high e (E)
    2: 11,  # B
    3: 7,   # G
    4: 2,   # D
    5: 9,   # A
    6: 4,   # low E
}


class Triad:
    """Represents a triad chord and can find positions on the fretboard."""

    def __init__(self, root, is_major=True):
        """Initialize a triad.

        Args:
            root: Root note name (e.g., 'C', 'A', 'F#', 'Bb')
            is_major: True for major triad, False for minor triad
        """
        self.root = root
        self.is_major = is_major

        # Get the chromatic index of the root
        if root not in ENHARMONIC_MAP:
            raise ValueError(f"Invalid root note: {root}")

        root_index = ENHARMONIC_MAP[root]

        # Calculate the note indices for the triad
        intervals = MAJOR_INTERVALS if is_major else MINOR_INTERVALS
        self.note_indices = [(root_index + interval) % 12 for interval in intervals]

    def get_note_names(self, inversion=0):
        """Get the note names in order for a given inversion.

        Args:
            inversion: 0 for root position, 1 for 1st inversion, 2 for 2nd inversion

        Returns:
            List of three note names in order (lowest to highest string: 4, 3, 2)
        """
        # Rotate the note indices based on inversion
        # inversion 0: [root, 3rd, 5th]
        # inversion 1: [3rd, 5th, root]
        # inversion 2: [5th, root, 3rd]
        rotated = self.note_indices[inversion:] + self.note_indices[:inversion]

        # Convert back to note names (find matching note name for each index)
        note_names = []
        for idx in rotated:
            # Find a note name that matches this index
            for note_name, note_idx in ENHARMONIC_MAP.items():
                if note_idx == idx:
                    note_names.append(note_name)
                    break

        return note_names

    def find_position(self, inversion=0, start_fret=0, max_fret=12):
        """Find the first position for this triad on strings 2, 3, 4.

        Args:
            inversion: 0 for root position, 1 for 1st inversion, 2 for 2nd inversion
            start_fret: Minimum fret to start searching from
            max_fret: Maximum fret to search up to

        Returns:
            List of (string_num, fret_num) tuples for the three notes,
            or None if no position found in range
        """
        # Get the note indices for this inversion
        rotated = self.note_indices[inversion:] + self.note_indices[:inversion]

        # We want to find positions on strings 4, 3, 2 (lowest to highest)
        # String 4 gets the first note, string 3 gets the second, string 2 gets the third
        target_strings = [4, 3, 2]

        # Start searching from start_fret
        for fret_4 in range(start_fret, max_fret + 1):
            # Calculate the note at this fret on string 4
            string_4_open = GUITAR_TUNING[4]
            note_at_fret_4 = (string_4_open + fret_4) % 12

            # Check if this matches the first note of our inversion
            if note_at_fret_4 == rotated[0]:
                # Now find the second and third notes on strings 3 and 2
                # Search within a reasonable range (same fret or nearby)
                position = [(4, fret_4)]

                # Find second note on string 3
                string_3_open = GUITAR_TUNING[3]
                for fret_3 in range(max(0, fret_4 - 3), min(max_fret + 1, fret_4 + 5)):
                    note_at_fret_3 = (string_3_open + fret_3) % 12
                    if note_at_fret_3 == rotated[1]:
                        position.append((3, fret_3))
                        break

                # Find third note on string 2
                string_2_open = GUITAR_TUNING[2]
                for fret_2 in range(max(0, fret_4 - 3), min(max_fret + 1, fret_4 + 5)):
                    note_at_fret_2 = (string_2_open + fret_2) % 12
                    if note_at_fret_2 == rotated[2]:
                        position.append((2, fret_2))
                        break

                # If we found all three notes, return the position
                if len(position) == 3:
                    return position

        return None

    def get_quality_name(self):
        """Get the quality name (major or minor)."""
        return "major" if self.is_major else "minor"

    def get_inversion_name(self, inversion):
        """Get the inversion name."""
        if inversion == 0:
            return "no-inversion"
        elif inversion == 1:
            return "1st-inversion"
        elif inversion == 2:
            return "2nd-inversion"
        else:
            raise ValueError(f"Invalid inversion: {inversion}")

    def format_answer(self, inversion=0):
        """Format the expected answer for this triad.

        Args:
            inversion: 0 for root position, 1 for 1st inversion, 2 for 2nd inversion

        Returns:
            String like "c e g" or "c e a"
        """
        notes = self.get_note_names(inversion)
        # Convert to lowercase for display
        return " ".join(note.lower() for note in notes)


def parse_triad_spec(spec):
    """Parse a triad specification like 'C major' or 'A minor'.

    Args:
        spec: String like 'C major', 'A minor', 'F# major', 'Bb minor'

    Returns:
        Tuple of (root, is_major)
    """
    parts = spec.strip().split()
    if len(parts) != 2:
        raise ValueError(f"Invalid triad spec: {spec}")

    root = parts[0]
    quality = parts[1].lower()

    if quality not in ['major', 'minor']:
        raise ValueError(f"Invalid quality: {quality}")

    is_major = (quality == 'major')
    return root, is_major
