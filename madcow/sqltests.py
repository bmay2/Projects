import unittest
import exercises
import sqlite3

sender, username, password = '***REMOVED***@messaging.sprintpcs.com', '***REMOVED***', '***REMOVED***'
recipient, gmail_user, gmail_pwd = '***REMOVED***@messaging.sprintpcs.com', '***REMOVED***@gmail.com', '***REMOVED***'

class SqlTableCreationTests(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(':memory:')
        self.conn.row_factory = sqlite3.Row
        self.c = self.conn.cursor()

    def testCreateHxTable(self):
        exercises.createhxtable(self.c)
        squathxtable = self.c.execute("SELECT * FROM sqlite_master").fetchone()
        self.assertIsNotNone(squathxtable)

class SqlInsertTests(unittest.TestCase):

    def setUp(self):
        self.conn = sqlite3.connect(':memory:')
        self.conn.row_factory = sqlite3.Row
        self.c = self.conn.cursor()
        exercises.check_all_tables(self.c)
        exercises.insertintohxtable(1, 0, 0, self.c)
        exercises.insertintohxtable(1, 0, 0, self.c)
        exercises.insertintohxtable(1, 0, 0, self.c)
        
    def testInsertIntoHxTable(self):
        squathx = self.c.execute("SELECT * FROM ExerciseHx WHERE ExerciseID=1").fetchone()
        self.assertEqual(squathx['Success'], 0)

    def testGetMax(self):
        maxsquat5 = exercises.get_five_rep_max(1, self.c)
        self.assertEqual(maxsquat5, 135)

    def testCheckBadTable(self):
        bad_table = exercises.check_if_table_exists('nope', self.c)
        self.assertIsNone(bad_table)

    def testCheckGoodTable(self):
        good_table = exercises.check_if_table_exists('Exercises', self.c)
        self.assertIsNotNone(good_table)

    def testCheckFailures(self):
        self.assertEqual(1, 2)




def main():
    unittest.main()

if __name__ == '__main__':
    main()
