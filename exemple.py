import pytz
from transportutils import driver
# date Is in GMT -taken from GPS system for exemple
GMT = pytz.timezone('UTC')
#take a working interval of 3days - what a heroic driver!!!
dd = driver.DriverDates(datetime.now(GMT) - timedelta(days=3), datetime.now(GMT))
# iterate on every days
for day in dd.days:
    # print start and end of "day"
    print day.startOfDay,"---", day.endOfDay
    # night time
    print "night : ",day.nighttimedelta
    #day time
    print "day : ",day.daytimedelta
    print "totaly time : ", day.nighttimedelta + day.daytimedelta