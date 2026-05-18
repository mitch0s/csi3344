from datetime import datetime, timedelta, timezone


def timestamp_utc(h:int=0, m:int=0, s:int=0, timestamp:str=None):
    """
    returns ISO 8601 timestamp: e.g. "2026-05-11T04:37:21+00:00", adjusted by arguments. 
    If a timestamp argument is supplied it will use that as the base timestamp rather than now()
    """
    if timestamp is not None : timestamp = datetime.fromisoformat(timestamp)
    else : timestamp = datetime.now(timezone.utc)
    return (timestamp + timedelta(hours=h, minutes=m, seconds=s)).isoformat(timespec='seconds')

