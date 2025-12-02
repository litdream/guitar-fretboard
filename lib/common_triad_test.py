"""Unit tests for the common_triad module."""

import pytest
from common_triad import (
    Triad, parse_triad_spec, MAJOR_INTERVALS, MINOR_INTERVALS, GUITAR_TUNING
)


class TestTriadInitialization:
    """Test Triad class initialization."""

    def test_c_major_initialization(self):
        """C major triad should initialize correctly."""
        triad = Triad('C', is_major=True)
        assert triad.root == 'C'
        assert triad.is_major is True
        # C major: C=0, E=4, G=7
        assert triad.note_indices == [0, 4, 7]

    def test_a_minor_initialization(self):
        """A minor triad should initialize correctly."""
        triad = Triad('A', is_major=False)
        assert triad.root == 'A'
        assert triad.is_major is False
        # A minor: A=9, C=0, E=4
        assert triad.note_indices == [9, 0, 4]

    def test_d_major_initialization(self):
        """D major triad should initialize correctly."""
        triad = Triad('D', is_major=True)
        assert triad.root == 'D'
        assert triad.is_major is True
        # D major: D=2, F#=6, A=9
        assert triad.note_indices == [2, 6, 9]

    def test_invalid_root_note(self):
        """Invalid root note should raise ValueError."""
        with pytest.raises(ValueError, match="Invalid root note"):
            Triad('X', is_major=True)


class TestTriadNoteNames:
    """Test get_note_names method for different inversions."""

    def test_c_major_root_position(self):
        """C major no-inversion: C E G."""
        triad = Triad('C', is_major=True)
        notes = triad.get_note_names(inversion=0)
        # Should be C, E, G (or enharmonic equivalents)
        assert len(notes) == 3
        # Check the chromatic indices match
        from diatonic import ENHARMONIC_MAP
        indices = [ENHARMONIC_MAP[note] for note in notes]
        assert indices == [0, 4, 7]

    def test_c_major_first_inversion(self):
        """C major 1st-inversion: E G C."""
        triad = Triad('C', is_major=True)
        notes = triad.get_note_names(inversion=1)
        assert len(notes) == 3
        # Should be E, G, C
        from diatonic import ENHARMONIC_MAP
        indices = [ENHARMONIC_MAP[note] for note in notes]
        assert indices == [4, 7, 0]

    def test_c_major_second_inversion(self):
        """C major 2nd-inversion: G C E."""
        triad = Triad('C', is_major=True)
        notes = triad.get_note_names(inversion=2)
        assert len(notes) == 3
        # Should be G, C, E
        from diatonic import ENHARMONIC_MAP
        indices = [ENHARMONIC_MAP[note] for note in notes]
        assert indices == [7, 0, 4]

    def test_a_minor_root_position(self):
        """A minor no-inversion: A C E."""
        triad = Triad('A', is_major=False)
        notes = triad.get_note_names(inversion=0)
        assert len(notes) == 3
        # Should be A, C, E
        from diatonic import ENHARMONIC_MAP
        indices = [ENHARMONIC_MAP[note] for note in notes]
        assert indices == [9, 0, 4]

    def test_a_minor_first_inversion(self):
        """A minor 1st-inversion: C E A."""
        triad = Triad('A', is_major=False)
        notes = triad.get_note_names(inversion=1)
        assert len(notes) == 3
        # Should be C, E, A
        from diatonic import ENHARMONIC_MAP
        indices = [ENHARMONIC_MAP[note] for note in notes]
        assert indices == [0, 4, 9]

    def test_a_minor_second_inversion(self):
        """A minor 2nd-inversion: E A C."""
        triad = Triad('A', is_major=False)
        notes = triad.get_note_names(inversion=2)
        assert len(notes) == 3
        # Should be E, A, C
        from diatonic import ENHARMONIC_MAP
        indices = [ENHARMONIC_MAP[note] for note in notes]
        assert indices == [4, 9, 0]


class TestTriadFindPosition:
    """Test find_position method."""

    def test_c_major_root_position_found(self):
        """C major root position should find a valid position."""
        triad = Triad('C', is_major=True)
        position = triad.find_position(inversion=0)
        assert position is not None
        assert len(position) == 3
        # Should return (string, fret) tuples for strings 4, 3, 2
        assert position[0][0] == 4  # String 4
        assert position[1][0] == 3  # String 3
        assert position[2][0] == 2  # String 2

    def test_a_minor_first_inversion_found(self):
        """A minor 1st inversion should find a valid position."""
        triad = Triad('A', is_major=False)
        position = triad.find_position(inversion=1)
        assert position is not None
        assert len(position) == 3
        assert position[0][0] == 4  # String 4
        assert position[1][0] == 3  # String 3
        assert position[2][0] == 2  # String 2

    def test_position_notes_match(self):
        """Position should match the expected notes on the fretboard."""
        triad = Triad('C', is_major=True)
        position = triad.find_position(inversion=0)

        # Verify the notes at each position match C E G
        from diatonic import ENHARMONIC_MAP
        expected_indices = [0, 4, 7]  # C, E, G

        for i, (string_num, fret_num) in enumerate(position):
            open_note = GUITAR_TUNING[string_num]
            note_at_fret = (open_note + fret_num) % 12
            assert note_at_fret == expected_indices[i]

    def test_position_within_range(self):
        """Position should respect max_fret limit."""
        triad = Triad('C', is_major=True)
        position = triad.find_position(inversion=0, max_fret=5)

        if position is not None:
            for string_num, fret_num in position:
                assert fret_num <= 5


class TestTriadHelperMethods:
    """Test helper methods."""

    def test_get_quality_name_major(self):
        """Major triad should return 'major'."""
        triad = Triad('C', is_major=True)
        assert triad.get_quality_name() == 'major'

    def test_get_quality_name_minor(self):
        """Minor triad should return 'minor'."""
        triad = Triad('A', is_major=False)
        assert triad.get_quality_name() == 'minor'

    def test_get_inversion_name_root(self):
        """Inversion 0 should return 'no-inversion'."""
        triad = Triad('C', is_major=True)
        assert triad.get_inversion_name(0) == 'no-inversion'

    def test_get_inversion_name_first(self):
        """Inversion 1 should return '1st-inversion'."""
        triad = Triad('C', is_major=True)
        assert triad.get_inversion_name(1) == '1st-inversion'

    def test_get_inversion_name_second(self):
        """Inversion 2 should return '2nd-inversion'."""
        triad = Triad('C', is_major=True)
        assert triad.get_inversion_name(2) == '2nd-inversion'

    def test_get_inversion_name_invalid(self):
        """Invalid inversion should raise ValueError."""
        triad = Triad('C', is_major=True)
        with pytest.raises(ValueError, match="Invalid inversion"):
            triad.get_inversion_name(3)

    def test_format_answer_c_major_root(self):
        """C major root position answer format."""
        triad = Triad('C', is_major=True)
        answer = triad.format_answer(inversion=0)
        # Should be lowercase notes separated by spaces
        assert isinstance(answer, str)
        notes = answer.split()
        assert len(notes) == 3
        # All should be lowercase
        assert all(note.islower() or '#' in note or 'b' in note for note in notes)

    def test_format_answer_a_minor_first(self):
        """A minor 1st inversion answer format."""
        triad = Triad('A', is_major=False)
        answer = triad.format_answer(inversion=1)
        assert isinstance(answer, str)
        notes = answer.split()
        assert len(notes) == 3


class TestParseTriadSpec:
    """Test parse_triad_spec function."""

    def test_parse_c_major(self):
        """Parse 'C major' correctly."""
        root, is_major = parse_triad_spec('C major')
        assert root == 'C'
        assert is_major is True

    def test_parse_a_minor(self):
        """Parse 'A minor' correctly."""
        root, is_major = parse_triad_spec('A minor')
        assert root == 'A'
        assert is_major is False

    def test_parse_f_sharp_major(self):
        """Parse 'F# major' correctly."""
        root, is_major = parse_triad_spec('F# major')
        assert root == 'F#'
        assert is_major is True

    def test_parse_bb_minor(self):
        """Parse 'Bb minor' correctly."""
        root, is_major = parse_triad_spec('Bb minor')
        assert root == 'Bb'
        assert is_major is False

    def test_parse_with_extra_spaces(self):
        """Parse with extra spaces should work."""
        root, is_major = parse_triad_spec('  C   major  ')
        assert root == 'C'
        assert is_major is True

    def test_parse_invalid_format(self):
        """Invalid format should raise ValueError."""
        with pytest.raises(ValueError, match="Invalid triad spec"):
            parse_triad_spec('C')

    def test_parse_invalid_quality(self):
        """Invalid quality should raise ValueError."""
        with pytest.raises(ValueError, match="Invalid quality"):
            parse_triad_spec('C augmented')


class TestTriadConstants:
    """Test module constants."""

    def test_major_intervals(self):
        """Major intervals should be 0, 4, 7 semitones."""
        assert MAJOR_INTERVALS == [0, 4, 7]

    def test_minor_intervals(self):
        """Minor intervals should be 0, 3, 7 semitones."""
        assert MINOR_INTERVALS == [0, 3, 7]

    def test_guitar_tuning_defined(self):
        """Guitar tuning should define all 6 strings."""
        assert len(GUITAR_TUNING) == 6
        assert all(i in GUITAR_TUNING for i in range(1, 7))
        # Standard tuning: E(4), B(11), G(7), D(2), A(9), E(4)
        assert GUITAR_TUNING[1] == 4   # high e
        assert GUITAR_TUNING[2] == 11  # B
        assert GUITAR_TUNING[3] == 7   # G
        assert GUITAR_TUNING[4] == 2   # D
        assert GUITAR_TUNING[5] == 9   # A
        assert GUITAR_TUNING[6] == 4   # low E


class TestTriadRealWorldExamples:
    """Test real-world triad examples from the game."""

    def test_c_major_no_inversion(self):
        """C major, no-inversion should produce 'c e g'."""
        triad = Triad('C', is_major=True)
        answer = triad.format_answer(0)
        # The answer should contain c, e, g in some form
        notes = answer.split()
        from diatonic import ENHARMONIC_MAP
        # Get indices to verify correctness
        indices = [ENHARMONIC_MAP[note.upper().replace('B', 'Bb').replace('#', '#')]
                   if len(note) > 1 else ENHARMONIC_MAP[note.upper()] for note in notes]
        assert indices == [0, 4, 7]

    def test_a_minor_first_inversion(self):
        """A minor, 1st-inversion should produce 'c e a'."""
        triad = Triad('A', is_major=False)
        answer = triad.format_answer(1)
        notes = answer.split()
        from diatonic import ENHARMONIC_MAP
        # Get indices to verify correctness
        indices = [ENHARMONIC_MAP[note.upper().replace('B', 'Bb').replace('#', '#')]
                   if len(note) > 1 else ENHARMONIC_MAP[note.upper()] for note in notes]
        assert indices == [0, 4, 9]
