"""
Sample Tests
"""

from django.test import SimpleTestCase

from app import calc


class CalccTests(SimpleTestCase):
    """Test the calc module"""

    def test_add_number(self):
        """Test adding numbers together"""
        res = calc.add(5, 6)

        self.assertEqual(res, 11)

    def test_subtract_numbers(self):
        """Test subractiong numbers"""
        res = calc.subtract(10, 15)

        self.assertEqual(res, 5)
