"""
Note it would be better to more rigorously test each instance of values for start, end and stages instead of comparing the string value
for the class. Since speed is prioritiesed this will be done at a later stage as the string method is "good" enough for now.
"""

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
#Basic functionality

    def testTimeIntervalsSize(self):
        self.assertTrue(self.day1.size()==self.size)

    def testTimeIntervalsToString(self):
        correct_string = "stage: 5 from 00:00 to 05:00\nstage: 3 from 05:00 to 20:00\nstage: 4 from 20:00 to 00:00\n"
        self.assertTrue(str(self.day1)==correct_string)

    def testTimeIntervalsOutputAsJson(self):
        output_json = self.day1.outputDayJson()
        correct_json = """{"0": {"stage": 5, "start": "00:00", "end": "05:00"}, "1": {"stage": 3, "start": "05:00", "end": "20:00"}, "2": {"stage": 4, "start": "20:00", "end": "00:00"}}"""
        self.assertEqual(output_json, correct_json)

    def testTimeIntervalsOutputAsDict(self):
        output_dict = self.day1.outputDayDict()
        correct_dict = {0: {"stage": 5, "start": "00:00", "end": "05:00"}, 1: {"stage": 3, "start": "05:00", "end": "20:00"}, 2: {"stage": 4, "start": "20:00", "end": "00:00"}}
        self.assertEqual(output_dict, correct_dict)

#######################################################################################################################################
#Constructor Test

    def testTimeIntervalsCreatorNotDayStart(self):
        start_time2 = ["01:00","05:00","20:00"]
        end_time2 = ["05:00","20:00","00:00"]
        stages2 = [5,3,4]
        day2 = TimeIntervals(start_time2,end_time2,stages2)
        correct_string = "stage: 0 from 00:00 to 01:00\nstage: 5 from 01:00 to 05:00\nstage: 3 from 05:00 to 20:00\nstage: 4 from 20:00 to 00:00\n"
        self.assertTrue(str(day2)==correct_string)

    def testTimeIntervalsCreatorNotDayEnd(self):
        start_time2 = ["00:00","05:00","20:00"]
        end_time2 = ["05:00","20:00","23:00"]
        stages2 = [5,3,4]
        day2 = TimeIntervals(start_time2,end_time2,stages2)
        correct_string = "stage: 5 from 00:00 to 05:00\nstage: 3 from 05:00 to 20:00\nstage: 4 from 20:00 to 23:00\nstage: 0 from 23:00 to 00:00\n"
        self.assertTrue(str(day2)==correct_string)

    def testTimeIntervalsCreatorMismatchIntervalTimes(self):
        start_time2 = ["00:00","10:00","20:00"]
        end_time2 = ["05:00","20:00","23:00"]
        stages2 = [5,3,4]
        self.assertRaisesRegex(ValueError, "Time intervals do not align", TimeIntervals, start_time2,end_time2,stages2)

    def testTimeIntervalsCreatorMismatchIntervalStartAndEndBothIncorrect(self):
        start_time2 = ["01:00","05:00","20:00"]
        end_time2 = ["05:00","20:00","23:00"]
        stages2 = [5,3,4]
        day2 = TimeIntervals(start_time2,end_time2,stages2)
        correct_string = "stage: 0 from 00:00 to 01:00\nstage: 5 from 01:00 to 05:00\nstage: 3 from 05:00 to 20:00\nstage: 4 from 20:00 to 23:00\nstage: 0 from 23:00 to 00:00\n"
        self.assertTrue(str(day2)==correct_string)


#######################################################################################################################################
#Simple helper function test

    def testTimeIntervalsIsValidTrueCase(self):
        self.assertTrue(self.day1.isValid())
    
    def testTimeIntervalsIsValidFalseCaseIntervalMismatch(self):
        start_time2 = ["00:00","10:00","20:00"]
        end_time2 = ["05:00","20:00","00:00"]
        stages2 = [5,3,4]
        # For TimeIntervals full_day must be false, else an error in creator function is thrown instead, improve by testing with 
        # FitInInterval
        day2 = TimeIntervals(start_time2,end_time2,stages2,False)
        self.assertFalse(day2.isValid())

    def testTimeIntervalsIsValidFalseCaseStart0EndNMismatch(self):
        start_time2 = ["00:00","05:00","20:00"]
        end_time2 = ["05:00","20:00","23:00"]
        stages2 = [5,3,4]
        # For TimeIntervals full_day must be false, else an error in creator function is thrown instead, improve by testing with 
        # FitInInterval
        day2 = TimeIntervals(start_time2,end_time2,stages2,False)
        self.assertFalse(day2.isValid())

    def testTimeIntervalsIsCompleteDayTrueCase(self):
        self.assertTrue(self.day1.isCompleteDay())

    def testTimeIntervalsIsCompleteDayFalseCaseStartDayNotZero(self):
        start_time2 = ["02:00","05:00","20:00"]
        end_time2 = ["05:00","20:00","00:00"]
        stages2 = [5,3,4]
        # For TimeIntervals full_day must be false, else an error in creator function is thrown instead, improve by testing with 
        # FitInInterval
        day2 = TimeIntervals(start_time2,end_time2,stages2,False)
        self.assertFalse(day2.isValid())

    def testTimeIntervalsIsCompleteDayFalseCaseEndDayNotZero(self):
        start_time2 = ["00:00","05:00","20:00"]
        end_time2 = ["05:00","20:00","23:00"]
        stages2 = [5,3,4]
        # For TimeIntervals full_day must be false, else an error in creator function is thrown instead, improve by testing with 
        # FitInInterval
        day2 = TimeIntervals(start_time2,end_time2,stages2,False)
        self.assertFalse(day2.isValid())

########################################################################################################################################
#IsInterval tests

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
#InOneInterval tests

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
#InMultipleIntervals tests     

    def testTimeIntervalsInMultipleIntervalsTwoIntervalsStartEqualEndEqual(self):
        ss = datetime.strptime('00:00', '%H:%M')
        ee = datetime.strptime('20:00', '%H:%M')
        intervals =  self.day1.inMultipleIntervals(ss,ee)
        self.assertTrue(intervals[0]==0)
        self.assertTrue(intervals[1]==1)

    def testTimeIntervalsInMultipleIntervalsTwoIntervalsStartEqualLessThanEnd(self):
        ss = datetime.strptime('00:00', '%H:%M')
        ee = datetime.strptime('10:00', '%H:%M')
        intervals =  self.day1.inMultipleIntervals(ss,ee)
        self.assertTrue(intervals[0]==0)
        self.assertTrue(intervals[1]==1)
    
    def testTimeIntervalsInMultipleIntervalsTwoIntervalsGreaterThanStartEndEqual(self):
        ss = datetime.strptime('03:00', '%H:%M')
        ee = datetime.strptime('20:00', '%H:%M')
        intervals =  self.day1.inMultipleIntervals(ss,ee)
        self.assertTrue(intervals[0]==0)
        self.assertTrue(intervals[1]==1)

    def testTimeIntervalsInMultipleIntervalsTwoIntervalsGreaterThanStartLessThanEnd(self):
        ss = datetime.strptime('03:00', '%H:%M')
        ee = datetime.strptime('10:00', '%H:%M')
        intervals =  self.day1.inMultipleIntervals(ss,ee)
        self.assertTrue(intervals[0]==0)
        self.assertTrue(intervals[1]==1)

    def testTimeIntervalsInMultipleIntervalsTwoIntervalsStartEqualEndEqualAndEndInLastInterval(self):
        ss = datetime.strptime('05:00', '%H:%M')
        ee = datetime.strptime('23:59', '%H:%M')
        intervals =  self.day1.inMultipleIntervals(ss,ee)
        self.assertTrue(intervals[0]==1)
        self.assertTrue(intervals[1]==2)

    def testTimeIntervalsInMultipleIntervalsTwoIntervalsStartEqualLessThanEndAndEndInLastInterval(self):
        ss = datetime.strptime('05:00', '%H:%M')
        ee = datetime.strptime('22:00', '%H:%M')
        intervals =  self.day1.inMultipleIntervals(ss,ee)
        self.assertTrue(intervals[0]==1)
        self.assertTrue(intervals[1]==2)
    
    def testTimeIntervalsInMultipleIntervalsTwoIntervalsGreaterThanStartEndEqualAndEndInLastInterval(self):
        ss = datetime.strptime('12:00', '%H:%M')
        ee = datetime.strptime('23:59', '%H:%M')
        intervals =  self.day1.inMultipleIntervals(ss,ee)
        self.assertTrue(intervals[0]==1)
        self.assertTrue(intervals[1]==2)

    def testTimeIntervalsInMultipleIntervalsTwoIntervalsGreaterThanStartLessThanEndAndEndInLastInterval(self):
        ss = datetime.strptime('12:00', '%H:%M')
        ee = datetime.strptime('22:00', '%H:%M')
        intervals =  self.day1.inMultipleIntervals(ss,ee)
        self.assertTrue(intervals[0]==1)
        self.assertTrue(intervals[1]==2)

    def testTimeIntervalsInMultipleIntervalsTwoIntervalsSpansEntireDay(self):
        ss = datetime.strptime('00:00', '%H:%M')
        ee = datetime.strptime('23:59', '%H:%M')
        intervals =  self.day1.inMultipleIntervals(ss,ee)
        self.assertTrue(intervals[0]==0)
        self.assertTrue(intervals[1]==self.day1.size()-1)
    
    
########################################################################################################################################    
#FitNewInterval where new interval is contained in a single existing interval
    
    def testTimeIntervalsExistingSlotChangeStageValue(self):
        ss = '05:00'
        ee = '20:00'
        correct_string = "stage: 5 from 00:00 to 05:00\nstage: 1 from 05:00 to 20:00\nstage: 4 from 20:00 to 00:00\n"
        self.day1.fitNewInterval(1,ss,ee)
        self.assertTrue(str(self.day1)==correct_string)
        
    def testTimeIntervalsInsertInOneIntervalEqualStartLessThanEnd(self):
        ss = '05:00'
        ee = '09:00'
        correct_string = "stage: 5 from 00:00 to 05:00\nstage: 1 from 05:00 to 09:00\nstage: 3 from 09:00 to 20:00\nstage: 4 from 20:00 to 00:00\n"
        self.day1.fitNewInterval(1,ss,ee)
        self.assertTrue(str(self.day1)==correct_string)
        
    def testTimeIntervalsInsertInOneIntervalGreaterThanStartEqualEnd(self):
        ss = '10:00'
        ee = '20:00'
        correct_string = "stage: 5 from 00:00 to 05:00\nstage: 3 from 05:00 to 10:00\nstage: 1 from 10:00 to 20:00\nstage: 4 from 20:00 to 00:00\n"
        self.day1.fitNewInterval(1,ss,ee)
        self.assertTrue(str(self.day1)==correct_string)

    def testTimeIntervalsInsertInOneIntervalGreaterThanStartLessThanEnd(self):
        ss = '08:00'
        ee = '17:00'
        correct_string = "stage: 5 from 00:00 to 05:00\nstage: 3 from 05:00 to 08:00\nstage: 1 from 08:00 to 17:00\nstage: 3 from 17:00 to 20:00\nstage: 4 from 20:00 to 00:00\n"
        self.day1.fitNewInterval(1,ss,ee)
        self.assertTrue(str(self.day1)==correct_string)

    def testTimeIntervalsInsertInOneIntervalEqualStartLessThanEndFirstSlot(self):
        ss = '00:00'
        ee = '04:00'
        correct_string = "stage: 1 from 00:00 to 04:00\nstage: 5 from 04:00 to 05:00\nstage: 3 from 05:00 to 20:00\nstage: 4 from 20:00 to 00:00\n"
        self.day1.fitNewInterval(1,ss,ee)
        self.assertTrue(str(self.day1)==correct_string)
        
    def testTimeIntervalsInsertInOneIntervalGreaterThanStartEqualEndFirstSlot(self):
        ss = '02:00'
        ee = '05:00'
        correct_string = "stage: 5 from 00:00 to 02:00\nstage: 1 from 02:00 to 05:00\nstage: 3 from 05:00 to 20:00\nstage: 4 from 20:00 to 00:00\n"
        self.day1.fitNewInterval(1,ss,ee)
        self.assertTrue(str(self.day1)==correct_string)

    def testTimeIntervalsInsertInOneIntervalGreaterThanStartLessThanEndFirstSlot(self):
        ss = '02:00'
        ee = '04:00'
        correct_string = "stage: 5 from 00:00 to 02:00\nstage: 1 from 02:00 to 04:00\nstage: 5 from 04:00 to 05:00\nstage: 3 from 05:00 to 20:00\nstage: 4 from 20:00 to 00:00\n"
        self.day1.fitNewInterval(1,ss,ee)
        self.assertTrue(str(self.day1)==correct_string)

    def testTimeIntervalsInsertInOneIntervalEqualStartLessThanEndLastSlot(self):
        ss = '20:00'
        ee = '22:00'
        correct_string = "stage: 5 from 00:00 to 05:00\nstage: 3 from 05:00 to 20:00\nstage: 1 from 20:00 to 22:00\nstage: 4 from 22:00 to 00:00\n"
        self.day1.fitNewInterval(1,ss,ee)
        self.assertTrue(str(self.day1)==correct_string)
        
    def testTimeIntervalsInsertInOneIntervalGreaterThanStartEqualEndLastSlot(self):
        ss = '23:00'
        ee = '00:00'
        correct_string = "stage: 5 from 00:00 to 05:00\nstage: 3 from 05:00 to 20:00\nstage: 4 from 20:00 to 23:00\nstage: 1 from 23:00 to 00:00\n"
        self.day1.fitNewInterval(1,ss,ee)
        self.assertTrue(str(self.day1)==correct_string)

    def testTimeIntervalsInsertInOneIntervalGreaterThanStartLessThanEndLastSlot(self):
        ss = '21:00'
        ee = '23:00'
        correct_string = "stage: 5 from 00:00 to 05:00\nstage: 3 from 05:00 to 20:00\nstage: 4 from 20:00 to 21:00\nstage: 1 from 21:00 to 23:00\nstage: 4 from 23:00 to 00:00\n"
        self.day1.fitNewInterval(1,ss,ee)
        self.assertTrue(str(self.day1)==correct_string)
#########################################################################################################################################
#FitNewInterval where new interval is contained in a single existing interval


    def testTimeIntervalsInsertInMultipleIntervalsNewSpansTwoIntervalsReduceToOne(self):
        ss = '00:00'
        ee = '20:00'
        correct_string = "stage: 1 from 00:00 to 20:00\nstage: 4 from 20:00 to 00:00\n"
        self.day1.fitNewInterval(1,ss,ee)
        self.assertTrue(str(self.day1)==correct_string)

    def testTimeIntervalsInsertInMultipleIntervalsNewSpansTwoIntervalsReduceToOneLastSlot(self):
        ss = '05:00'
        ee = '00:00'
        correct_string = "stage: 5 from 00:00 to 05:00\nstage: 1 from 05:00 to 00:00\n"
        self.day1.fitNewInterval(1,ss,ee)
        self.assertTrue(str(self.day1)==correct_string)
        
    def testTimeIntervalsInsertInMultipleIntervalsNewEqualStartLessThanEnd(self):
        ss = '00:00'
        ee = '15:00'
        correct_string = "stage: 1 from 00:00 to 15:00\nstage: 3 from 15:00 to 20:00\nstage: 4 from 20:00 to 00:00\n"
        self.day1.fitNewInterval(1,ss,ee)
        self.assertTrue(str(self.day1)==correct_string)

    def testTimeIntervalsInsertInMultipleIntervalsNewGreaterThanStartEqualEnd(self):
        ss = '04:00'
        ee = '20:00'
        correct_string = "stage: 5 from 00:00 to 04:00\nstage: 1 from 04:00 to 20:00\nstage: 4 from 20:00 to 00:00\n"
        self.day1.fitNewInterval(1,ss,ee)
        self.assertTrue(str(self.day1)==correct_string)

    def testTimeIntervalsInsertInMultipleIntervalsNewGreaterThanStartLessThanEnd(self):
        ss = '04:00'
        ee = '15:00'
        correct_string = "stage: 5 from 00:00 to 04:00\nstage: 1 from 04:00 to 15:00\nstage: 3 from 15:00 to 20:00\nstage: 4 from 20:00 to 00:00\n"
        self.day1.fitNewInterval(1,ss,ee)
        self.assertTrue(str(self.day1)==correct_string)
        
    
    def testTimeIntervalsInsertInMultipleIntervalsNewEqualStartLessThanEndLastSlot(self):
        ss = '05:00'
        ee = '21:00'
        correct_string = "stage: 5 from 00:00 to 05:00\nstage: 1 from 05:00 to 21:00\nstage: 4 from 21:00 to 00:00\n"
        self.day1.fitNewInterval(1,ss,ee)
        self.assertTrue(str(self.day1)==correct_string)

    def testTimeIntervalsInsertInMultipleIntervalsNewGreaterThanStartEqualEndLastSlot(self):
        ss = '11:00'
        ee = '00:00'
        correct_string = "stage: 5 from 00:00 to 05:00\nstage: 3 from 05:00 to 11:00\nstage: 1 from 11:00 to 00:00\n"
        self.day1.fitNewInterval(1,ss,ee)
        self.assertTrue(str(self.day1)==correct_string)

    def testTimeIntervalsInsertInMultipleIntervalsNewGreaterThanStartLessThanEndLastSlot(self):
        ss = '11:00'
        ee = '23:00'
        correct_string = "stage: 5 from 00:00 to 05:00\nstage: 3 from 05:00 to 11:00\nstage: 1 from 11:00 to 23:00\nstage: 4 from 23:00 to 00:00\n"
        self.day1.fitNewInterval(1,ss,ee)
        self.assertTrue(str(self.day1)==correct_string)

    def testTimeIntervalsInsertInMultipleIntervalsNewSpansMoreThanTwoIntervalsReduceToOne(self):
        start_time2 = ["00:00","06:00","08:00","12:00","13:00","17:00","21:00"]
        end_time2 = ["06:00","08:00","12:00","13:00","17:00","21:00","00:00"]
        stages2 = [5,6,3,3,4,7,5]
        day2 = TimeIntervals(start_time2,end_time2,stages2)
        ss = '06:00'
        ee = '21:00'

        correct_string = "stage: 5 from 00:00 to 06:00\nstage: 1 from 06:00 to 21:00\nstage: 5 from 21:00 to 00:00\n"
        day2.fitNewInterval(1,ss,ee)
        self.assertTrue(str(day2)==correct_string)

    def testTimeIntervalsInsertInMultipleIntervalsNewEqualStartLessThanEnd(self):
        start_time2 = ["00:00","06:00","08:00","12:00","13:00","17:00","21:00"]
        end_time2 = ["06:00","08:00","12:00","13:00","17:00","21:00","00:00"]
        stages2 = [5,6,3,3,4,7,5]
        day2 = TimeIntervals(start_time2,end_time2,stages2)
        ss = '06:00'
        ee = '19:00'

        correct_string = "stage: 5 from 00:00 to 06:00\nstage: 1 from 06:00 to 19:00\nstage: 7 from 19:00 to 21:00\nstage: 5 from 21:00 to 00:00\n"
        day2.fitNewInterval(1,ss,ee)
        self.assertTrue(str(day2)==correct_string)

    def testTimeIntervalsInsertInMultipleIntervalsNewGreaterThanStartEqualEnd(self):
        start_time2 = ["00:00","06:00","08:00","12:00","13:00","17:00","21:00"]
        end_time2 = ["06:00","08:00","12:00","13:00","17:00","21:00","00:00"]
        stages2 = [5,6,3,3,4,7,5]
        day2 = TimeIntervals(start_time2,end_time2,stages2)
        ss = '08:00'
        ee = '20:00'

        correct_string = "stage: 5 from 00:00 to 06:00\nstage: 6 from 06:00 to 08:00\nstage: 1 from 08:00 to 20:00\nstage: 7 from 20:00 to 21:00\nstage: 5 from 21:00 to 00:00\n"
        day2.fitNewInterval(1,ss,ee)
        self.assertTrue(str(day2)==correct_string)

    def testTimeIntervalsInsertInMultipleIntervalsNewGreaterThanStartLessThanEnd(self):
        start_time2 = ["00:00","06:00","08:00","12:00","13:00","17:00","21:00"]
        end_time2 = ["06:00","08:00","12:00","13:00","17:00","21:00","00:00"]
        stages2 = [5,6,3,3,4,7,5]
        day2 = TimeIntervals(start_time2,end_time2,stages2)
        ss = '08:00'
        ee = '19:00'

        correct_string = "stage: 5 from 00:00 to 06:00\nstage: 6 from 06:00 to 08:00\nstage: 1 from 08:00 to 19:00\nstage: 7 from 19:00 to 21:00\nstage: 5 from 21:00 to 00:00\n"
        day2.fitNewInterval(1,ss,ee)
        self.assertTrue(str(day2)==correct_string)

    def testTimeIntervalsInsertInMultipleIntervalsEntireDay(self):
        ss = '00:00'
        ee = '00:00'
        correct_string = "stage: 1 from 00:00 to 00:00\n"
        self.day1.fitNewInterval(1,ss,ee)
        self.assertTrue(str(self.day1)==correct_string)

         
