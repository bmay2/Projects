import unittest
import exercises
import datetime

class DateTests(unittest.TestCase):

	def setUp(self):
		self.datewithzeroes = datetime.date(2013,3,1)
		self.datewithnozeroes = datetime.date(2012,12,31)

	def testDateTimesWithZeroesMatch(self):
		testdatestring = "20130301"
		prepareddatestring = exercises.preparedateinsert(self.datewithzeroes)
		self.assertEqual(prepareddatestring, testdatestring)

	def testDateTimesWithNoZeroesMatch(self):
		testdatestring = "20121231"
		prepareddatestring = exercises.preparedateinsert(self.datewithnozeroes)
		self.assertEqual(prepareddatestring, testdatestring)

	def testDateTimesWithZeroesDoNotMatch(self):
		testdatestring = "20040908"
		prepareddatestring = exercises.preparedateinsert(self.datewithzeroes)
		self.assertNotEqual(prepareddatestring, testdatestring)

	def testDateTimesWithNoZeroesDoNotMatch(self):
		testdatestring = "20041218"
		prepareddatestring = exercises.preparedateinsert(self.datewithnozeroes)
		self.assertNotEqual(prepareddatestring, testdatestring)

	def testDateComparison(self):
		first_date = exercises.preparedateinsert(datetime.date(2004, 9, 8))
		second_date = exercises.preparedateinsert(datetime.date(2004, 10, 8))
		earliest_date = min(first_date, second_date)
		latest_date = max(first_date, second_date)
		self.assertTrue(first_date == earliest_date and second_date == latest_date)

	def testAuditDateWeekDayZeroes(self):
		self.datestring = "20130301"
		test = exercises.auditdateoutput(self.datestring)
		self.assertEqual(test, 4)

	def testAuditDateWeekDayNoZeroes(self):
		self.datestring = "20130228"
		test = exercises.auditdateoutput(self.datestring)
		self.assertEqual(test, 3)

def main():
	unittest.main()

if __name__ == '__main__':
	main()