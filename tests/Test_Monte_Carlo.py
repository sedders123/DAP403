import unittest
from src.montecarlo import get_totals


class TestMonteCarlo(unittest.TestCase):
    """Tests for `montecarlo.py`."""

    def test_get_totals(self):
        """Is five successfully determined to be prime?"""
        self.assertTrue(is_prime(5))


if __name__ == '__main__':
    unittest.main()
