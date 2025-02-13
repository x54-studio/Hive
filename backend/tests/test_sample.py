import unittest

# Przykładowa funkcja, którą będziemy testować
def add(a, b):
    return a + b

class TestAddFunction(unittest.TestCase):
    def test_add_integers(self):
        self.assertEqual(add(2, 3), 5)

    def test_add_strings(self):
        self.assertEqual(add("Hello ", "World"), "Hello World")

if __name__ == '__main__':
    unittest.main()
