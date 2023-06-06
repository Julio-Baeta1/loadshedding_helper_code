import unittest
from datetime import datetime
from TimeIntervals import TimeIntervals

class TestTimeIntervals(unittest.TestCase):

    def setUp(self):
        start_time1 = ["00:00","05:00","20:00"]
        end_time1 = ["05:00","20:00","00:00"]
        stages1 = [5,3,4]
        self.day1 = TimeIntervals(start_time1,end_time1,stages1)
        self.size = len(end_time1)

    def tearDown(self):
        del self.day1
        del self.size 

#######################################################################################################################################     

    def testTimeIntervalsSize(self):
        self.assertTrue(self.day1.size()==self.size)

    def testTimeIntervalsToString(self):
        correct_string = "stage: 5 from 00:00 to 05:00\nstage: 3 from 05:00 to 20:00\nstage: 4 from 20:00 to 00:00\n"
        self.assertTrue(str(self.day1)==correct_string)

#######################################################################################################################################

    def testTimeIntervalsIsValidTrueCase(self):
        self.assertTrue(self.day1.isValid())
    
    def testTimeIntervalsIsValidFalseCaseIntervalMismatch(self):
        start_time2 = ["00:00","10:00","20:00"]
        end_time2 = ["05:00","20:00","00:00"]
        stages2 = [5,3,4]
        day2 = TimeIntervals(start_time2,end_time2,stages2)
        self.assertFalse(day2.isValid())

    def testTimeIntervalsIsValidFalseCaseStart0EndNMismatch(self):
        start_time2 = ["00:00","05:00","20:00"]
        end_time2 = ["05:00","20:00","23:00"]
        stages2 = [5,3,4]
        day2 = TimeIntervals(start_time2,end_time2,stages2)
        self.assertFalse(day2.isValid())

    def testTimeIntervalsIsCompleteDayTrueCase(self):
        self.assertTrue(self.day1.isCompleteDay())

    def testTimeIntervalsIsCompleteDayFalseCaseStartDayNotZero(self):
        start_time2 = ["02:00","05:00","20:00"]
        end_time2 = ["05:00","20:00","00:00"]
        stages2 = [5,3,4]
        day2 = TimeIntervals(start_time2,end_time2,stages2)
        self.assertFalse(day2.isValid())

    def testTimeIntervalsIsCompleteDayFalseCaseEndDayNotZero(self):
        start_time2 = ["00:00","05:00","20:00"]
        end_time2 = ["05:00","20:00","23:00"]
        stages2 = [5,3,4]
        day2 = TimeIntervals(start_time2,end_time2,stages2)
        self.assertFalse(day2.isValid())

########################################################################################################################################

    def testTimeIntervalsIsIntervalTrueCase(self):
        ss = datetime.strptime('05:00', '%H:%M')
        ee = datetime.strptime('20:00', '%H:%M')
        is_interval,i =  self.day1.isInterval(ss,ee)
        self.assertTrue(is_interval)
        self.assertTrue(i==1)

    def testTimeIntervalsIsIntervalTrueCaseFirstSlot(self):
        ss = datetime.strptime('00:00', '%H:%M')
        ee = datetime.strptime('05:00', '%H:%M')
        is_interval,i =  self.day1.isInterval(ss,ee)
        self.assertTrue(is_interval)
        self.assertTrue(i==0)

    def testTimeIntervalsIsIntervalTrueCaseEndSlot(self):
        ss = datetime.strptime('20:00', '%H:%M')
        ee = datetime.strptime('23:59', '%H:%M')
        is_interval,i =  self.day1.isInterval(ss,ee)
        self.assertTrue(is_interval)
        self.assertTrue(i==self.size-1)

    def testTimeIntervalsIsIntervalFalseCaseStartEqualToAnInterval(self):
        ss = datetime.strptime('05:00', '%H:%M')
        ee = datetime.strptime('09:00', '%H:%M')
        is_interval,i =  self.day1.isInterval(ss,ee)
        self.assertFalse(is_interval)
        self.assertTrue(i==self.size)

    def testTimeIntervalsIsIntervalFalseCaseEndEqualToAnInterval(self):
        ss = datetime.strptime('09:00', '%H:%M')
        ee = datetime.strptime('20:00', '%H:%M')
        is_interval,i =  self.day1.isInterval(ss,ee)
        self.assertFalse(is_interval)
        self.assertTrue(i==self.size)

    def testTimeIntervalsIsIntervalFalseCaseNotEqualToIntervalStartOrEnd(self):
        ss = datetime.strptime('09:00', '%H:%M')
        ee = datetime.strptime('17:00', '%H:%M')
        is_interval,i =  self.day1.isInterval(ss,ee)
        self.assertFalse(is_interval)
        self.assertTrue(i==self.size)

########################################################################################################################################

    def testTimeIntervalsInOneIntervalTrueCaseStartEqual(self):
        ss = datetime.strptime('05:00', '%H:%M')
        ee = datetime.strptime('11:00', '%H:%M')
        is_in_one_interval,i =  self.day1.inOneInterval(ss,ee)
        self.assertTrue(is_in_one_interval)
        self.assertTrue(i==1)

    def testTimeIntervalsInOneIntervalTrueCaseEndEqual(self):
        ss = datetime.strptime('16:00', '%H:%M')
        ee = datetime.strptime('20:00', '%H:%M')
        is_in_one_interval,i =  self.day1.inOneInterval(ss,ee)
        self.assertTrue(is_in_one_interval)
        self.assertTrue(i==1)

    def testTimeIntervalsInOneIntervalTrueCaseInbetweenStartAndEnd(self):
        ss = datetime.strptime('10:00', '%H:%M')
        ee = datetime.strptime('14:00', '%H:%M')
        is_in_one_interval,i =  self.day1.inOneInterval(ss,ee)
        self.assertTrue(is_in_one_interval)
        self.assertTrue(i==1)

    def testTimeIntervalsInOneIntervalFalseCaseStartEqualGreaterThanEnd(self):
        ss = datetime.strptime('05:00', '%H:%M')
        ee = datetime.strptime('22:00', '%H:%M')
        is_in_one_interval,i =  self.day1.inOneInterval(ss,ee)
        self.assertFalse(is_in_one_interval)
        self.assertTrue(i==self.size)

    def testTimeIntervalsInOneIntervalFalseCaseGreaterThanStartGreaterThanEnd(self):
        ss = datetime.strptime('10:00', '%H:%M')
        ee = datetime.strptime('22:00', '%H:%M')
        is_in_one_interval,i =  self.day1.inOneInterval(ss,ee)
        self.assertFalse(is_in_one_interval)
        self.assertTrue(i==self.size)

########################################################################################################################################    
    def testTimeIntervalsExistingSlotChangeStageValue(self):
        ss = datetime.strptime('05:00', '%H:%M')
        ee = datetime.strptime('20:00', '%H:%M')
        correct_string = "stage: 5 from 00:00 to 05:00\nstage: 1 from 05:00 to 20:00\nstage: 4 from 20:00 to 00:00\n"
        self.day1.fitNewInterval(1,ss,ee)
        self.assertTrue(str(self.day1)==correct_string)
        
    def testTimeIntervalsInsertInOneIntervalEqualStartLessThanEnd(self):
        ss = datetime.strptime('05:00', '%H:%M')
        ee = datetime.strptime('09:00', '%H:%M')
        correct_string = "stage: 5 from 00:00 to 05:00\nstage: 1 from 05:00 to 09:00\nstage: 3 from 09:00 to 20:00\nstage: 4 from 20:00 to 00:00\n"
        self.day1.fitNewInterval(1,ss,ee)
        self.assertTrue(str(self.day1)==correct_string)
        
    def testTimeIntervalsInsertInOneIntervalGreaterThanStartEqualEnd(self):
        ss = datetime.strptime('10:00', '%H:%M')
        ee = datetime.strptime('20:00', '%H:%M')
        correct_string = "stage: 5 from 00:00 to 05:00\nstage: 3 from 05:00 to 10:00\nstage: 1 from 10:00 to 20:00\nstage: 4 from 20:00 to 00:00\n"
        self.day1.fitNewInterval(1,ss,ee)
        self.assertTrue(str(self.day1)==correct_string)

    def testTimeIntervalsInsertInOneIntervalGreaterThanStartLessThanEnd(self):
        ss = datetime.strptime('08:00', '%H:%M')
        ee = datetime.strptime('17:00', '%H:%M')
        correct_string = "stage: 5 from 00:00 to 05:00\nstage: 3 from 05:00 to 08:00\nstage: 1 from 08:00 to 17:00\nstage: 3 from 17:00 to 20:00\nstage: 4 from 20:00 to 00:00\n"
        self.day1.fitNewInterval(1,ss,ee)
        self.assertTrue(str(self.day1)==correct_string)

    def testTimeIntervalsInsertInOneIntervalEqualStartLessThanEndFirstSlot(self):
        ss = datetime.strptime('00:00', '%H:%M')
        ee = datetime.strptime('04:00', '%H:%M')
        correct_string = "stage: 1 from 00:00 to 04:00\nstage: 5 from 04:00 to 05:00\nstage: 3 from 05:00 to 20:00\nstage: 4 from 20:00 to 00:00\n"
        self.day1.fitNewInterval(1,ss,ee)
        self.assertTrue(str(self.day1)==correct_string)
        
    def testTimeIntervalsInsertInOneIntervalGreaterThanStartEqualEndFirstSlot(self):
        ss = datetime.strptime('02:00', '%H:%M')
        ee = datetime.strptime('05:00', '%H:%M')
        correct_string = "stage: 5 from 00:00 to 02:00\nstage: 1 from 02:00 to 05:00\nstage: 3 from 05:00 to 20:00\nstage: 4 from 20:00 to 00:00\n"
        self.day1.fitNewInterval(1,ss,ee)
        self.assertTrue(str(self.day1)==correct_string)

    def testTimeIntervalsInsertInOneIntervalGreaterThanStartLessThanEndFirstSlot(self):
        ss = datetime.strptime('02:00', '%H:%M')
        ee = datetime.strptime('04:00', '%H:%M')
        correct_string = "stage: 5 from 00:00 to 02:00\nstage: 1 from 02:00 to 04:00\nstage: 5 from 04:00 to 05:00\nstage: 3 from 05:00 to 20:00\nstage: 4 from 20:00 to 00:00\n"
        self.day1.fitNewInterval(1,ss,ee)
        self.assertTrue(str(self.day1)==correct_string)

    def testTimeIntervalsInsertInOneIntervalEqualStartLessThanEndLastSlot(self):
        ss = datetime.strptime('20:00', '%H:%M')
        ee = datetime.strptime('22:00', '%H:%M')
        correct_string = "stage: 5 from 00:00 to 05:00\nstage: 3 from 05:00 to 20:00\nstage: 1 from 20:00 to 22:00\nstage: 4 from 22:00 to 00:00\n"
        self.day1.fitNewInterval(1,ss,ee)
        self.assertTrue(str(self.day1)==correct_string)
        
    def testTimeIntervalsInsertInOneIntervalGreaterThanStartEqualEndLastSlot(self):
        ss = datetime.strptime('23:00', '%H:%M')
        ee = datetime.strptime('00:00', '%H:%M')
        correct_string = "stage: 5 from 00:00 to 05:00\nstage: 3 from 05:00 to 20:00\nstage: 4 from 20:00 to 23:00\nstage: 1 from 23:00 to 00:00\n"
        self.day1.fitNewInterval(1,ss,ee)
        self.assertTrue(str(self.day1)==correct_string)

    def testTimeIntervalsInsertInOneIntervalGreaterThanStartLessThanEndLastSlot(self):
        ss = datetime.strptime('21:00', '%H:%M')
        ee = datetime.strptime('23:00', '%H:%M')
        correct_string = "stage: 5 from 00:00 to 05:00\nstage: 3 from 05:00 to 20:00\nstage: 4 from 20:00 to 21:00\nstage: 1 from 21:00 to 23:00\nstage: 4 from 23:00 to 00:00\n"
        self.day1.fitNewInterval(1,ss,ee)
        self.assertTrue(str(self.day1)==correct_string)
        
