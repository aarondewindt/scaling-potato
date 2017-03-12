import unittest

from scaling_potato.scaling_potato_c import test_opencv


class TestCppExtension(unittest.TestCase):
    def test_printing(self):
        test_opencv()


if __name__ == '__main__':
    unittest.main()
