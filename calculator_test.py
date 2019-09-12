import unittest
from calculator import Calculator


class CalculatorTest(unittest.TestCase):
    
    def setUp(self):
        self.calc = Calculator()

    # def test_simple_addition(self):
    #     self.assertEqual(self.calc.calculate('2 + 2'), 4)

    def test_parenthesis(self):
        self.assertEqual(self.calc.calculate('5*8+(2+2)/2'), 42)

if __name__ == "__main__":
    unittest.main()