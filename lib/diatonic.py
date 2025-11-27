"""This lib provides lookup table and information of key and scale.

"""

# Standard chromatic scales
all_notes_sharp = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
all_notes_flat =  ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']

# Extended chromatic scales for exotic keys (includes double sharps/flats)
all_notes_sharp_extended = ['B#', 'C#', 'D', 'D#', 'E', 'E#', 'F#', 'G', 'G#', 'A', 'A#', 'B']
all_notes_flat_extended =  ['C', 'Db', 'D', 'Eb', 'Fb', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'Cb']

# Enharmonic equivalents map - maps note names to their chromatic index (0-11)
ENHARMONIC_MAP = {
    'C': 0, 'B#': 0,
    'C#': 1, 'Db': 1,
    'D': 2,
    'D#': 3, 'Eb': 3,
    'E': 4, 'Fb': 4,
    'F': 5, 'E#': 5,
    'F#': 6, 'Gb': 6,
    'G': 7,
    'G#': 8, 'Ab': 8,
    'A': 9,
    'A#': 10, 'Bb': 10,
    'B': 11, 'Cb': 11,
}


def note_to_index(note_name):
    """Convert a note name to its chromatic index (0-11).

    Args:
        note_name: Note name like 'C', 'F#', 'Gb', 'E#', etc.

    Returns:
        Integer 0-11 representing the chromatic index

    Raises:
        ValueError: If note_name is not recognized
    """
    if note_name in ENHARMONIC_MAP:
        return ENHARMONIC_MAP[note_name]
    raise ValueError(f"Invalid note name: {note_name}")

# Keys that traditionally use flats (adjust this lookup table as needed)
# F, Bb, Eb, Ab, Db, Gb, Cb use flats
# Their relative minors also use flats: Dmin, Gmin, Cmin, Fmin, Bbmin, Ebmin, Abmin
FLAT_KEYS = {
    'F', 'Bb', 'Eb', 'Ab', 'Db', 'Gb', 'Cb',
    'Dmin', 'Gmin', 'Cmin', 'Fmin', 'Bbmin', 'Ebmin', 'Abmin'
}

# Keys that need extended chromatic scales (exotic keys with E#, B#, Cb, Fb)
EXTENDED_SHARP_KEYS = {'F#', 'C#', 'F#min', 'C#min', 'D#min', 'A#min'}
EXTENDED_FLAT_KEYS = {'Gb', 'Cb', 'Ebmin', 'Abmin'}

# Whole step (W) = 2 semitones, Half step (H) = 1 semitone
# Major scale pattern: W-W-H-W-W-W-H
MAJOR_INTERVALS = [2, 2, 1, 2, 2, 2, 1]

# Minor scale pattern (natural minor): W-H-W-W-H-W-W
MINOR_INTERVALS = [2, 1, 2, 2, 1, 2, 2]

class Diatonic:
    def __init__(self, keyname: str):
        """Initialize a diatonic scale for a given key.

        Examples:
            Diatonic("C") -> scale = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
            Diatonic("Amin") -> scale = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
            Diatonic("G") -> scale = ['G', 'A', 'B', 'C', 'D', 'E', 'F#']
            Diatonic("D") -> scale = ['D', 'E', 'F#', 'G', 'A', 'B', 'C#']
            Diatonic("F") -> scale = ['F', 'G', 'A', 'Bb', 'C', 'D', 'E']
            Diatonic("Dmin") -> scale = ['D', 'E', 'F', 'G', 'A', 'Bb', 'C']
        """
        self.keyname = keyname
        self.is_minor = keyname.endswith('min')

        # Determine root note and intervals
        if self.is_minor:
            root = keyname[:-3]  # Remove 'min' suffix
            intervals = MINOR_INTERVALS
        else:
            root = keyname
            intervals = MAJOR_INTERVALS

        # Determine whether to use flats or sharps based on tradition
        self.use_flats = keyname in FLAT_KEYS

        # Choose the appropriate chromatic scale (standard or extended)
        if keyname in EXTENDED_SHARP_KEYS:
            chromatic = all_notes_sharp_extended
        elif keyname in EXTENDED_FLAT_KEYS:
            chromatic = all_notes_flat_extended
        elif self.use_flats:
            chromatic = all_notes_flat
        else:
            chromatic = all_notes_sharp

        # Find the starting position using enharmonic-aware mapping
        start_idx = note_to_index(root)

        # Build the scale using the interval pattern
        self.scale = []
        current_idx = start_idx
        for interval in intervals:
            self.scale.append(chromatic[current_idx % 12])
            current_idx += interval


