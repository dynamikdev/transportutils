"""
Tools for calculate hours/periods of a Truck's driver 
Actually only valable in France

"""
from datetime import timedelta
from dateutil import rrule

import pytz
# GMT = pytz.timezone('UTC')
# fr = pytz.timezone('Europe/Paris')

ENDNIGHT = 6
STARTNIGHT = 21

class DriverDaysDates(object):
    """
    """
    def __init__(self,startOfDay,endOfDay):
        self.startOfDay = startOfDay
        self.endOfDay = endOfDay
        self.daytimedelta = self.nighttimedelta = timedelta()
        self.change = list(rrule.rrule(rrule.DAILY,
            byhour=(ENDNIGHT,STARTNIGHT),
            byminute=0,
            bysecond=0,
            dtstart=startOfDay,
            until=endOfDay))
        if len(list(self.change))==0 :
            #there no changing type
            if len(list(rrule.rrule(rrule.DAILY,
            byhour=0,
            byminute=0,
            bysecond=0,
            dtstart=self.startOfDay,
            until=self.endOfDay)))>0 or self.startOfDay.hour> STARTNIGHT or self.startOfDay.hour> ENDNIGHT :
                #there is midnight or start is in night so everything is nigth
                self.nighttimedelta = abs(self.endOfDay -self.startOfDay)
                self.daytimedelta = timedelta()
            else:
                #overwise is a day
                self.nighttimedelta = timedelta()
                self.daytimedelta = abs(self.endOfDay -self.startOfDay)
        else:
            self.calcthedelta()
        

    def calcthedelta(self):
        lstdate = [self.startOfDay] + list(self.change) + [self.endOfDay]
        # print lstdate
        for k in range(1, len(lstdate)):
            # print k,lstdate[k-1],lstdate[k]
            isNight = False
            if lstdate[k-1] in self.change: #start from a change
                if lstdate[k-1].hour == STARTNIGHT:
                    isNight = True
            if lstdate[k] in self.change: #start from a change
                if lstdate[k].hour == ENDNIGHT:
                    isNight = True
            if isNight:
                self.nighttimedelta += abs(lstdate[k] - lstdate[k-1])
            else:
                self.daytimedelta += abs(lstdate[k] - lstdate[k-1])


class DriverDates(object):
    """
    """
    DriverTimeZone = pytz.timezone('Europe/Paris')
    def __init__(self, datedeb, datefin):
        self.datedeb = datedeb.astimezone(self.DriverTimeZone)
        self.datefin = datefin.astimezone(self.DriverTimeZone)
        lstdate = [self.datedeb] + \
         list(rrule.rrule(rrule.DAILY,
            byhour=0,
            byminute=0,
            bysecond=0,
            dtstart=self.datedeb,
            until=self.datefin)) +\
             [self.datefin]
        self.days = [DriverDaysDates(lstdate[k-1], lstdate[k]) for k in range(1, len(lstdate))]    

