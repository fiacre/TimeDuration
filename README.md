TimeDuration
============

Pure Python module that handles stopwatch time rather than wallclock time

The TimeDuration module provides a Pure Python interface to the creation, manipulation and comparison
of time duration string.  E.g. if 3:21:45.3 and 3:22:30.1 represent stopwatch times, I don't want
to represent or store them as datetime objects but I do want to be able to compare them and
do simple calculations on such string such as find the average of a tuple of TimeDuration objects.
I'd also like to be able to say something like "3 weeks, 5 days 12 hours and 32 minutes" and be
able to convert that to minutes, seconds or hours and be able to convert strings that look like
durations of time to a normalized format.


After running setup.py, run test.py

There are examples of usage in the example.py file


Author Andrew Lee, fiacre.patrick@gmail.com

2012-03-16: update
    now can call to_timedelta and get back a datetime.timedelta object



