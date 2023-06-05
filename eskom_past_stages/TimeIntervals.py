from datetime import datetime

class TimeIntervals:
    """
    A class that contains consecutive time intervals of varying size for a day. A stage is allocated to each interval.
    The purpose of this class is to more easily facilitate changing of a given time interval set to a new that preserves the
    old information
    """

    def __init__(self,start,end,stages):
        """
        start: string list of interval starting times '17:00','20:00'
        end: string list of interval ending times '20:00','00:00'
        stages: corresponding load-shedding stage for each time interval
        """
        
        if len(start)==len(end) and len(end)==len(stages):
            #Start, end and stages lists must be of same size for valid intervals to form 
            
            self.start = [datetime.strptime(str_t, '%H:%M') for str_t in start]
            self.end = [datetime.strptime(str_t, '%H:%M') for str_t in end]
            self.stages = stages
            self.num_slots = len(start)
            self.zero = datetime.strptime('00:00', '%H:%M')# time interval equivalent to 0
            
        else:
            raise ValueError('Time interval creations list dims do not match')  

 
    def isValid(self):
        """
        Tests that the ith start time matches the i+1th end time for all times
        """
        
        is_valid = True
        
        if self.start[0] != self.end[self.num_slots-1]:
            #cyclical 
            is_valid = False
        
        for i in range(self.num_slots-1):
            if self.end[i] != self.start[i+1]:
                is_valid = False
                
        return is_valid
    
    def isCompleteDay(self):
        """
        Tests that first interval starts at 00:00 and that all intervals are valid
        """
        
        day = False
        
        if self.start[0] == self.zero:
            day = True
            
        if self.isValid() and day:
            return True
        else:
            return False
        
    def size(self):
        """
        returns number of time intervals
        """
        
        return self.num_slots
    
    def isInterval(self, start, end):
        """
        Tests if the given time interval corresponds to an existing one.
        Returns: True if it does and the interval's index.
                 False otherwise and a num outside the interval index range.
        """
        
        for i in range(self.num_slots):
            if self.start[i] == start and self.end[i] == end:
                return True,i
            
        return False,self.num_slots
    
    def inOneInterval(self, start, end):
        """
        Tests if the given time interval is completely contained within an existing one.
        Returns: True if it does and the interval's index.
                 False otherwise and the next interval's index.
        """
        
        for i in range(self.num_slots-1):
            if self.start[i] <= start and self.end[i] >= end:
                return True,i
                       
        return False,self.num_slots+1
    
    def fitNewInterval(self, stage, start, end):
        """
        Insert new time interval into set of existing intervals
        """
        
        #start = pd.to_datetime(start,format= '%H:%M') 
        #end = pd.to_datetime(end,format= '%H:%M')
        in_interval,i = self.isInterval(start,end)
        
        if in_interval:
        #Is an existing interval
            self.stages[i] = stage
            
        else:
            one_interval,i = self.inOneInterval(start,end)
            
            if one_interval:
                #Fully contained within one interval
            
                if start == self.start[i]:
                    #Aligns to start of interval, insert one new time interval
                    
                    temp = self.end[i]
                    self.end[i] = end
                    self.start = self.start[:i+1] + [end] + self.start[i+1:]
                    self.end = self.end[:i+1] + [temp] + self.end[i+1:]
                    self.stages = self.stages[:i] + [stage] + self.stages[i:]
                    self.num_slots += 1
                
                elif end == self.end[i]:
                    #Aligns to end of interval, insert one new time interval
                    
                    self.end[i] = start
                    self.start = self.start[:i+1] + [start] + self.start[i+1:]
                    self.end = self.end[:i+1] + [end] + self.end[i+1:]
                    self.stages = self.stages[:i+1] + [stage] + self.stages[i+1:]
                    self.num_slots += 1
                
                else:
                    #Contained within interval, insert two new time intervals
                    temp = self.end[i]
                    self.end[i] = start
                    self.start = self.start[:i+1] + [start,end] + self.start[i+1:]
                    self.end = self.end[:i+1] + [end,temp] + self.end[i+1:]
                    self.stages = self.stages[:i+1] + [stage] + self.stages[i:]
                    self.num_slots += 2
            
                
        
    def __str__(self):
        
        print_string = ""
        for i in range(self.num_slots):
            print_string += "stage: "+str(self.stages[i])+" from "+str(self.start[i].strftime('%H:%M'))+" to "+ \
            str(self.end[i].strftime('%H:%M'))+ "\n"
        
        return print_string