import unittest
import exercises

class Tests(unittest.TestCase):

    def setUp(self):
        self.current_max = 175
        self.before4weeks = 2
        self.equal4weeks = 4
        self.after4weeks = 8

    def testBefore4WeeksTopSet(self):
        top_set = round(exercises.get_top_set(self.current_max, self.before4weeks))
        self.assertEqual(top_set, 166)
        
    def testEqual4WeeksTopSet(self):
        top_set = round(exercises.get_top_set(self.current_max, self.equal4weeks))
        self.assertEqual(top_set, 175)

    def testAfter4WeeksTopSet(self):
        top_set = round(exercises.get_top_set(self.current_max, self.after4weeks))
        self.assertEqual(top_set, 193)

    def testParseTextEmailSuccess(self):
        exercise, success = exercises.parse_text_email_for_success('Squat', '20130303 Sybyrn')
        self.assertEqual(success, 1)

    def testParseTextEmailDate(self):
        date = exercises.parse_text_email_for_date('20130303 Sybyrn')
        self.assertEqual(date, '20130303')

def main():
    unittest.main()

if __name__ == '__main__':
    main()