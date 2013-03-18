from datetime import timedelta, datetime, tzinfo
from time import gmtime, strftime


class GMT_8(tzinfo):
    def utcoffset(self, dt):
        return timedelta(hours=-8) + self.dst(dt)

    def dst(self, dt):
        d = datetime(dt.year, 4, 1)
        self.dston = d - timedelta(days=d.weekday() + 1)
        d = datetime(dt.year, 11, 1)
        self.dstoff = d - timedelta(days=d.weekday() + 1)
        if self.dston <= dt.replace(tzinfo=None) < self.dstoff:
            return timedelta(hours=1)
        else:
            return timedelta(0)

    def tzname(self, dt):
        return "GMT -8"


class GMT_5(tzinfo):

    def utcoffset(self, dt):
        return timedelta(hours=-5) + self.dst(dt)

    def dst(self, dt):
        d = datetime(dt.year, 4, 1)
        self.dston = d - timedelta(days=d.weekday() + 1)
        d = datetime(dt.year, 11, 1)
        self.dstoff = d - timedelta(days=d.weekday() + 1)
        if self.dston <= dt.replace(tzinfo=None) < self.dstoff:
            return timedelta(hours=1)
        else:
            return timedelta(0)

    def tzname(self, dt):
        return "GMT -5"


def convert_timezone(origin, from_tz, to_tz):
    try:
        if from_tz == "local()":
            from_tz = strftime("%Z", gmtime())
        if from_tz == "PST":
            from_tz = GMT_8()
        if to_tz == "EST":
            to_tz = GMT_5()

        origin = origin.replace(tzinfo=from_tz)
        new = origin.astimezone(to_tz)
        new = new.replace(
            tzinfo=None)  # remove offset-aware to be a offset-naive
        return new
    except:
        return origin

# dt2 = datetime(2012, 12, 21, 00, 19, 00, tzinfo=GMT_8())
# print dt2.dst()
# print dt2.utcoffset()
# dt3 = dt2.astimezone(GMT_5())
# print dt2.utctimetuple() == dt3.utctimetuple()
