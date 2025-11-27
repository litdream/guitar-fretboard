"""Unit tests for the Diatonic class."""

import pytest
from diatonic import Diatonic, FLAT_KEYS, MAJOR_INTERVALS, MINOR_INTERVALS


class TestDiatonicMajorKeys:
    """Test major key scale generation."""

    def test_c_major(self):
        """C major has no sharps or flats."""
        d = Diatonic("C")
        assert d.scale == ['C', 'D', 'E', 'F', 'G', 'A', 'B']
        assert d.is_minor is False
        assert d.keyname == "C"

    def test_g_major(self):
        """G major has one sharp (F#)."""
        d = Diatonic("G")
        assert d.scale == ['G', 'A', 'B', 'C', 'D', 'E', 'F#']
        assert d.use_flats is False

    def test_d_major(self):
        """D major has two sharps (F#, C#)."""
        d = Diatonic("D")
        assert d.scale == ['D', 'E', 'F#', 'G', 'A', 'B', 'C#']
        assert d.use_flats is False

    def test_a_major(self):
        """A major has three sharps (F#, C#, G#)."""
        d = Diatonic("A")
        assert d.scale == ['A', 'B', 'C#', 'D', 'E', 'F#', 'G#']
        assert d.use_flats is False

    def test_e_major(self):
        """E major has four sharps (F#, C#, G#, D#)."""
        d = Diatonic("E")
        assert d.scale == ['E', 'F#', 'G#', 'A', 'B', 'C#', 'D#']
        assert d.use_flats is False

    def test_f_major(self):
        """F major has one flat (Bb)."""
        d = Diatonic("F")
        assert d.scale == ['F', 'G', 'A', 'Bb', 'C', 'D', 'E']
        assert d.use_flats is True

    def test_b_major(self):
        """B major has five sharps (F#, C#, G#, D#, A#)."""
        d = Diatonic("B")
        assert d.scale == ['B', 'C#', 'D#', 'E', 'F#', 'G#', 'A#']
        assert d.use_flats is False

    def test_f_sharp_major(self):
        """F# major has six sharps (F#, C#, G#, D#, A#, E#)."""
        d = Diatonic("F#")
        assert d.scale == ['F#', 'G#', 'A#', 'B', 'C#', 'D#', 'E#']
        assert d.use_flats is False

    def test_c_sharp_major(self):
        """C# major has seven sharps (all notes are sharp)."""
        d = Diatonic("C#")
        assert d.scale == ['C#', 'D#', 'E#', 'F#', 'G#', 'A#', 'B#']
        assert d.use_flats is False

    def test_bb_major(self):
        """Bb major has two flats (Bb, Eb)."""
        d = Diatonic("Bb")
        assert d.scale == ['Bb', 'C', 'D', 'Eb', 'F', 'G', 'A']
        assert d.use_flats is True

    def test_eb_major(self):
        """Eb major has three flats (Bb, Eb, Ab)."""
        d = Diatonic("Eb")
        assert d.scale == ['Eb', 'F', 'G', 'Ab', 'Bb', 'C', 'D']
        assert d.use_flats is True

    def test_ab_major(self):
        """Ab major has four flats (Bb, Eb, Ab, Db)."""
        d = Diatonic("Ab")
        assert d.scale == ['Ab', 'Bb', 'C', 'Db', 'Eb', 'F', 'G']
        assert d.use_flats is True

    def test_db_major(self):
        """Db major has five flats (Bb, Eb, Ab, Db, Gb)."""
        d = Diatonic("Db")
        assert d.scale == ['Db', 'Eb', 'F', 'Gb', 'Ab', 'Bb', 'C']
        assert d.use_flats is True

    def test_gb_major(self):
        """Gb major has six flats (Bb, Eb, Ab, Db, Gb, Cb)."""
        d = Diatonic("Gb")
        assert d.scale == ['Gb', 'Ab', 'Bb', 'Cb', 'Db', 'Eb', 'F']
        assert d.use_flats is True

    def test_cb_major(self):
        """Cb major has seven flats (all notes are flat)."""
        d = Diatonic("Cb")
        assert d.scale == ['Cb', 'Db', 'Eb', 'Fb', 'Gb', 'Ab', 'Bb']
        assert d.use_flats is True


class TestDiatonicMinorKeys:
    """Test minor key scale generation."""

    def test_a_minor(self):
        """A minor has no sharps or flats (relative to C major)."""
        d = Diatonic("Amin")
        assert d.scale == ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        assert d.is_minor is True
        assert d.keyname == "Amin"

    def test_e_minor(self):
        """E minor has one sharp (F#) - relative to G major."""
        d = Diatonic("Emin")
        assert d.scale == ['E', 'F#', 'G', 'A', 'B', 'C', 'D']
        assert d.use_flats is False

    def test_d_minor(self):
        """D minor has one flat (Bb) - relative to F major."""
        d = Diatonic("Dmin")
        assert d.scale == ['D', 'E', 'F', 'G', 'A', 'Bb', 'C']
        assert d.use_flats is True

    def test_b_minor(self):
        """B minor has two sharps (F#, C#) - relative to D major."""
        d = Diatonic("Bmin")
        assert d.scale == ['B', 'C#', 'D', 'E', 'F#', 'G', 'A']
        assert d.use_flats is False

    def test_f_sharp_minor(self):
        """F# minor has three sharps (F#, C#, G#) - relative to A major."""
        d = Diatonic("F#min")
        assert d.scale == ['F#', 'G#', 'A', 'B', 'C#', 'D', 'E']
        assert d.use_flats is False

    def test_c_sharp_minor(self):
        """C# minor has four sharps (F#, C#, G#, D#) - relative to E major."""
        d = Diatonic("C#min")
        assert d.scale == ['C#', 'D#', 'E', 'F#', 'G#', 'A', 'B']
        assert d.use_flats is False

    def test_g_sharp_minor(self):
        """G# minor has five sharps (F#, C#, G#, D#, A#) - relative to B major."""
        d = Diatonic("G#min")
        assert d.scale == ['G#', 'A#', 'B', 'C#', 'D#', 'E', 'F#']
        assert d.use_flats is False

    def test_d_sharp_minor(self):
        """D# minor has six sharps (F#, C#, G#, D#, A#, E#) - relative to F# major."""
        d = Diatonic("D#min")
        assert d.scale == ['D#', 'E#', 'F#', 'G#', 'A#', 'B', 'C#']
        assert d.use_flats is False

    def test_a_sharp_minor(self):
        """A# minor has seven sharps (all sharp) - relative to C# major."""
        d = Diatonic("A#min")
        assert d.scale == ['A#', 'B#', 'C#', 'D#', 'E#', 'F#', 'G#']
        assert d.use_flats is False

    def test_g_minor(self):
        """G minor has two flats (Bb, Eb) - relative to Bb major."""
        d = Diatonic("Gmin")
        assert d.scale == ['G', 'A', 'Bb', 'C', 'D', 'Eb', 'F']
        assert d.use_flats is True

    def test_c_minor(self):
        """C minor has three flats (Bb, Eb, Ab) - relative to Eb major."""
        d = Diatonic("Cmin")
        assert d.scale == ['C', 'D', 'Eb', 'F', 'G', 'Ab', 'Bb']
        assert d.use_flats is True

    def test_f_minor(self):
        """F minor has four flats (Bb, Eb, Ab, Db) - relative to Ab major."""
        d = Diatonic("Fmin")
        assert d.scale == ['F', 'G', 'Ab', 'Bb', 'C', 'Db', 'Eb']
        assert d.use_flats is True

    def test_bb_minor(self):
        """Bb minor has five flats (Bb, Eb, Ab, Db, Gb) - relative to Db major."""
        d = Diatonic("Bbmin")
        assert d.scale == ['Bb', 'C', 'Db', 'Eb', 'F', 'Gb', 'Ab']
        assert d.use_flats is True

    def test_eb_minor(self):
        """Eb minor has six flats (Bb, Eb, Ab, Db, Gb, Cb) - relative to Gb major."""
        d = Diatonic("Ebmin")
        assert d.scale == ['Eb', 'F', 'Gb', 'Ab', 'Bb', 'Cb', 'Db']
        assert d.use_flats is True

    def test_ab_minor(self):
        """Ab minor has seven flats (all flat) - relative to Cb major."""
        d = Diatonic("Abmin")
        assert d.scale == ['Ab', 'Bb', 'Cb', 'Db', 'Eb', 'Fb', 'Gb']
        assert d.use_flats is True


class TestDiatonicEdgeCases:
    """Test edge cases and error handling."""

    def test_invalid_root_note(self):
        """Invalid root note should raise ValueError."""
        with pytest.raises(ValueError, match="Invalid note name"):
            Diatonic("X")

    def test_invalid_minor_root_note(self):
        """Invalid minor root note should raise ValueError."""
        with pytest.raises(ValueError, match="Invalid note name"):
            Diatonic("Xmin")


class TestDiatonicConstants:
    """Test that module constants are properly defined."""

    def test_major_intervals_sum(self):
        """Major intervals should sum to 12 (one octave)."""
        assert sum(MAJOR_INTERVALS) == 12

    def test_minor_intervals_sum(self):
        """Minor intervals should sum to 12 (one octave)."""
        assert sum(MINOR_INTERVALS) == 12

    def test_flat_keys_defined(self):
        """FLAT_KEYS should contain expected keys."""
        assert 'F' in FLAT_KEYS
        assert 'Bb' in FLAT_KEYS
        assert 'Dmin' in FLAT_KEYS
        assert 'C' not in FLAT_KEYS
        assert 'G' not in FLAT_KEYS
