import unittest
from main import MultithreadMultiplicator, SquareMatrix

A = SquareMatrix([
   9,   2,   8,
   8,  -9,   6,
  -8,   1,  -2,
])
B = SquareMatrix([
   2,   6,   8,
   8,   9,  -2,
  -5,  -3,  -6,
])
C = SquareMatrix([
  - 6,   48,  20,
  -86,  -51,  46,
    2,  -33,  -54,
])


class TestStringMethods(unittest.TestCase):
  def test_single_thread(self):
    mul = MultithreadMultiplicator(1)

    C_test = mul.multiply(A, B)

    self.assertEqual(C_test, C)

  def test_multiple_threads(self):
    mul = MultithreadMultiplicator(16)

    C_test = mul.multiply(A, B)

    self.assertEqual(C_test, C)


if __name__ == '__main__':
    unittest.main()
