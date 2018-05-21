import unittest

import namer


class TestNamerEnglishFullName(unittest.TestCase):

    def testFirstLast(self):
        first = 'Robert'
        last = 'Jones'
        self.assertEqual(namer.english_full_name(
            first=first, last=last), first + ' ' + last)

    def testFirstLastMiddle(self):
        first = 'Robert'
        middle = 'Thomas'
        last = 'Jones'
        self.assertEqual(namer.english_full_name(
            first=first, last=last, middle=middle),
            first + ' ' + middle + ' ' + last)

    def testPrefixFirstLast(self):
        prefix = 'Dr'
        first = 'Robert'
        last = 'Jones'
        self.assertEqual(namer.english_full_name(
            first=first, last=last, prefix=prefix),
            prefix + ' ' + first + ' ' + last)

    def testPrefixFirstMiddleLast(self):
        prefix = 'Dr'
        first = 'Robert'
        middle = 'Thomas'
        last = 'Jones'
        self.assertEqual(namer.english_full_name(
            first=first, last=last, middle=middle, prefix=prefix),
            prefix + ' ' + first + ' ' + middle + ' ' + last)

    def testMissingFirstLast(self):
        self.assertRaises(ValueError, namer.english_full_name)

    def testMissingLast(self):
        self.assertRaises(ValueError, namer.english_full_name, first='John')

    def testMissingFirst(self):
        self.assertRaises(ValueError, namer.english_full_name, last='Doe')


if __name__ == '__main__':
    unittest.main()
