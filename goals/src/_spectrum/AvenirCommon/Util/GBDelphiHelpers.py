from datetime import timedelta, datetime

# A delphi datetime value is the (fractional) number of days since the epoch
# e.g. 42 minutes past the the UNIX epoch is 25569.029166666667 in Delphi terms.
DELPHI_EPOCH = datetime(1899, 12, 30)


def dateTime_toDelphi(dt):
    try:
        return (dt - DELPHI_EPOCH) / timedelta(days=1)
    except TypeError:
        delta = dt - DELPHI_EPOCH
        return delta.days + (delta.seconds + delta.microseconds / 1000000.0) / 24 / 3600


def dateTime_fromDelphi(dvalue):
    return DELPHI_EPOCH + timedelta(days=dvalue)
