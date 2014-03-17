import sys
import re
from datetime import timedelta

class TimeDuration (object) :
    """  
    Time Duration
    Accept string that looks like 'it ought to be time'
    turn into object that can be used on its own
    or as a datetime.timedelta object
    Use Case :
        time diff betwen 1d:12h:15m:7.72s and 2d:5h:12m:15.0s 
        for calulations involving timed events
    """
    TIME_UNITS = { "W" : ( "W", "wk", "week", "weeks" ), 
            "D" : ( "D", "d", "dd", "day", "days"),
            "H" : ( "H", "h", "hh", "hr", "hour", "hours"),
            "M" : ( "M", "m", "mm", "min", "mins", "minute", "minutes"),
            "S" : ( "S", "s", "ss", "sec", "secs", "second", "seconds")
        }

    def __init__ (self, time_string = None, verbose = 0) :
        self.DEBUG = False
        if verbose == 1 :
            self.DEBUG = True
        self.time_string = time_string
        self.wdhms_re = re.compile(
            r'week|wk|weeks|day|d|days|hr|hour|hours|hrs|min|sec|dd|hh|mm|ss|m|s', 
            re.IGNORECASE)
        self.hms_re = re.compile (r'\d*[:\-,\s+]?\d*[:\-,\s+]?\d*\.?\d?')
        self.weeks = 0
        self.days = 0
        self.hours = 0
        self.minutes = 0
        self.seconds = 0.0

        if time_string :
            if self.wdhms_re.search(self.time_string) :
                if self.DEBUG :
                    sys.stderr.write("DEBUG :__INIT__ : we have a funny string! Going Fuzzy!\n" + self.time_string)
                self._fuzzy_match()
            elif self.hms_re.search(self.time_string) :
                if self.DEBUG :
                    sys.stderr.write("DEBUG : __INIT__ : looks like a normalized string?\n" + self.time_string)
                self._string2time()
            else :
                print >>sys.stderr, "Unrecognized time string"
                raise AttributeError


    def to_timedelta(self, resolution=''):
        if resolution == 'seconds' or resolution =='':
            td = timedelta(seconds=int(round(self.to_seconds())))
            return td
        elif resolution == 'minutes':
            mins = 60*int(round(self.to_seconds()))
            td = timedelta(minutes=mins)
            return td
        elif resolution == 'hours':
            hours = 60*60*int(round(self._to_seconds()))
            td = timedelta(hours=hours)
            return td
        

    def to_seconds (self) :
        if self.DEBUG :
            sys.stderr.write('DEBUG (to_seconds):%d days %02d:%02d:%02.02f\n' % (self.days, self.hours, self.minutes, self.seconds))
        var = 0.0
        if self.weeks == 0 :
            var=float(self.seconds) + 60*int(self.minutes) + 3600*int(self.hours) + 86400*int(self.days)
        else :
            var=float(self.seconds) + 60*int(self.minutes) + 3600*int(self.hours) + 86400*int(self.days) + 604800*int(self.weeks)
        return float(var)
         

    def from_seconds (self) :
        if self.DEBUG :
            sys.stderr.write('DEBUG (from_seconds) : %02d:%02d:%02.02f\n' % (self.hours, self.minutes, self.seconds))
             
        return '%02d:%02d:%02.02f' % (self.hours, self.minutes, self.seconds)


    def to_minutes (self) :
        val = int(self.minutes) \
            + 60*int(self.hours) \
            + 24*60*int(self.days) \
            + 24*60*7*int(self.weeks) \
            + float(self.seconds)/60 
        return float(val)

        # "%d W %d D %02d:%02d:%02.02f" % 
        #   (self.weeks, self.days, self.hours, self.minutes, self.seconds)

    def to_hours (self) :
        var =  168*int(self.weeks)  \
            + int(self.hours) \
            + float(self.minutes)/60 \
            + float(self.seconds)/2600 \
            + 24*int(self.days)
        return float(var)

    def normalized (self, time_string = None) :
        if time_string != None :
            self.__init__(time_string)
        self._normalize_times()
        if (self.days > 0 or self.weeks > 0) :
            if self.weeks > 0 :
                self.days = 7*self.weeks
            return "%d D %02d:%02d:%02.02f" % (self.days, self.hours, self.minutes, self.seconds)
        else :
            return "%02d:%02d:%02.02f" % (self.hours, self.minutes, self.seconds)
        
        #if (self.days > 0 and self.hours <= 24 and self.minutes <= 60 and self.seconds <= 60) :
        #    return "%d D %02d:%02d:%02.02f" % (self.days, self.hours, self.minutes, self.seconds)
        #elif (self.hours <= 24 and self.minutes <= 60 and self.seconds <= 60):
        #    return "%02d:%02d:%02.02f" % (self.hours, self.minutes, self.seconds)
        #elif (self.minutes <= 60 and self.minutes <= 60) :
        #    return self.minutes + ":" + self.seconds
        #elif (self.seconds <= 60) :
        #    mins = self.minutes
        #    hrs, mins = divmod(mins, 60)
        #    self.hours = hrs
        #    self.minutes = mins
        #    return ""
        #else :
        #    return self.seconds
 

    def __repr__ (self) :
        """canonical DD:HH:MM:SS.ss representation"""
        hrs = 0.0
        hrs = float(self.hours) + self.days*24
        wks = 0.0
        wks = float(self.weeks) + self.days*7
        hrs += wks*24
        return '<TimeParse:  %02d:%02d:%02.02f' % (int(hrs), int(self.minutes), float(self.seconds))
    
    def __lt__(self, other) :
        if (isinstance (other, self.__class__)) :
            if self.to_seconds() < other.to_seconds() :
                return True
            else :
                return False
        else :
            raise TypeError
        
    def __le__(self, other) :
        if (isinstance (other, self.__class__)) :
            if self.to_seconds() <= other.to_seconds() :
                return True
            else :
                return False
        else : raise TypeError 
       
    def __eq__(self, other) :
        if (isinstance (other, self.__class__)) :
            if self.to_seconds() == other.to_seconds() :
                return True
            else :
                return False
        else : raise TypeError
       
    def __ne__(self, other) :
        if (isinstance (other, self.__class__)) :
            if self.to_seconds() != other.to_seconds() :
                return True
            else :
                return False
        else : raise TypeError
        
    def __gt__(self, other) :
        if (isinstance (other, self.__class__)) :
            if self.to_seconds() > other.to_seconds() :
                return True
            else :
                return False
        else : raise TypeError

    def __ge__(self, other) :
        if (isinstance (other, self.__class__)) :
            if self.to_seconds() >= other.to_seconds() :
                return True
            else :
                return False
        else : raise TypeError
       
    def __cmp__(self, other) :
        if (isinstance (other, self.__class__)) :
            return cmp( self.to_seconds(), other.to_seconds() )
        else : raise TypeError 

    def __add__(self, other) :
        if (isinstance (other, self.__class__)) :
            temp = TimeDuration()
            temp.seconds = self.to_seconds() + other.to_seconds()
            #return temp.from_seconds()
            temp._normalize_times()
            return temp
        else : 
            raise TypeError
        

    def __str__(self) :
        if (self.days == 0 and self.weeks == 0) :
            return '%02d:%02d:%02.02f' % (int(self.hours), int(self.minutes), float(self.seconds))
        elif (self.weeks == 0) :
            return '%02d D %02d:%02d:%02.02f' % (int(self.days), int(self.hours), int(self.minutes), float(self.seconds))
        else :
            total_days = (self.weeks)*7
            return '%02d D %02d:%02d:%02.02f' % (int (self.days), int(self.hours), int(self.minutes), float(self.seconds))

    def _fuzzy_match (self) :
        output = []
        if self.DEBUG :
            print >>sys.stderr, "DEBUG (fuzzy_match)  %s " % (self.time_string)

        """
        This will match 2 days, 12:34 -- 
        which might be the output of unix uptime command, note -- no seconds
        """
        colon_sep_match = re.compile(
                r'(\d+)\s*d(?:ays)?[:\-,\s+]+(\d+)[:\-,\s+]+(\d+)[:\-,\s+]*(\d*\.*\d*)', 
                    re.IGNORECASE)
        #colon_sep_re = re.compile(r'[:\-]')
        m = colon_sep_match.match(self.time_string)
        if m  :
            for g in m.groups() :
                if self.DEBUG : print >>sys.stderr, "DEBUG (fuzzy_match GROUPS ) %s " % (g)
            try :
                self.days = int(m.group(1))
            except ValueError : pass
            try :
                self.hours = int(m.group(2))
            except ValueError : pass
            try :
                self.minutes = int(m.group(3))
            except ValueError : pass
            try :
                self.seconds = float(m.group(4))
            except ValueError : pass
      
        for value in self.TIME_UNITS.keys() :
            for i in range(len(value)) :
                v = self.TIME_UNITS[value][i]
                s = "(\d+\.?\d*)\s*" + v
                search = re.search(s, self.time_string, re.IGNORECASE)
                if search != None :
                    output.append(search.group(1) + " " + value)
    
        for i in range(len(output)) :
            s = output[i].split(" ")
            if s[-1] == "W" :
                self.weeks = int(s[0])
            elif s[-1] == "D" :
                self.days = int(s[0])
            elif s[-1] == "H" :
                self.hours = int(s[0])
            elif s[-1] == "M" :
                self.minutes = int(s[0])
            elif s[-1] == "S" :
                self.seconds = float(s[0])

        if self.DEBUG : 
            sys.stderr.write("DEBUG (fuzzy_match) : %d %d %d %d %f\n" % (
             self.weeks, self.days, self.hours, self.minutes, self.seconds))
        self._normalize_times()


    def _string2time (self) :
        prog = re.compile('([\d+\.]+)')
        try :
            vals = prog.findall( self.time_string )
            if len(vals) == 4:
                self.days = int(vals[0]) 
                self.hours = int(vals[1])
                self.minutes = int(vals[2])
                self.seconds = float(vals[3])
            elif len(vals) == 3 :
                self.hours = int(vals[0])
                self.minutes = int(vals[1])
                self.seconds = float(vals[2])
            elif len(vals) == 2 :
                self.minutes = int(vals[0])
                self.seconds = float(vals[1])
            elif len(vals) == 1 :
                self.seconds = float(vals[0])
            else :
                raise AttributeError
        except AttributeError, e :
            sys.stderr.write("TimeParse Error : " + 
                self.time_string + 
                " does not look like a valid time string??\n ")
        except Exception, e :
            print >>sys.stderr, "TimeParse Error : " + str(e) 
            
        self._normalize_times()

    def _normalize_times (self) :
        if self.DEBUG : 
            sys.stderr.write('DEBUG (normalize_times) %d minutes %f seconds\n' % (
                self.minutes, self.seconds))
        d = min = sec = hrs = h = mins = 0.0
        if float(self.seconds) >= float(60.0) :
            min, sec = divmod(self.seconds, 60)
            hrs, mins = divmod(min, 60)
            self.seconds = sec
            self.minutes += min
            if self.DEBUG :
                sys.stderr.write(
                    'DEBUG (normalize_times) : %02d:%02d:%02.02f\n' % (
                        self.hours, self.minutes, self.seconds))
                sys.stderr.write(
                    'DEBUG (normalize_times) : %02d\n' % (hrs))
            if self.minutes >= 60 :
                h, self.minutes = divmod(self.minutes, 60)
                self.hours +=h
            else :
                self.hours += hrs
                self.seconds = sec
                if self.DEBUG :
                    sys.stderr.write(
                        'DEBUG (normalize_times) : %02d:%02d:%02.02f\n' % (
                            self.hours, self.minutes, self.seconds))
        
        elif int(self.minutes) >= int(60) :
            if self.DEBUG :
                sys.stderr.write( 
                    'DEBUG (normalize_times)  : %02d:%02d:%02.02f\n' % (
                        self.hours, self.minutes, self.seconds))
            hrs, mins = divmod(self.minutes, 60)
            self.minutes = mins
            self.hours += hrs

        elif ( self.days != 0 and self.hours >= 24 ) :
            if self.DEBUG :
                sys.stderr.write( 
                    'DEBUG (normalize_times)  : %d days %02d:%02d:%02.02f\n' % (
                        self.days, self.hours, self.minutes, self.seconds))
            d, hrs =  divmod(self.hours, 24)
            self.days += d
            self.hours = hrs
            
       

