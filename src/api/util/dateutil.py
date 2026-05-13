from datetime import datetime, timedelta, UTC

def timestamp_now_utc():
    """
    returns ISO 8601 timestamp: e.g. "2026-05-11T04:37:21+00:00"
    """
    return datetime.now(UTC).isoformat(timespec='seconds')


def timestamp_now_utc(h: int = 0, m: int = 0, s: int = 0):
    """
    returns ISO 8601 timestamp adjusted by offset arguments
    """
    return (datetime.now(UTC) + timedelta(hours=h, minutes=m, seconds=s)).isoformat(timespec='seconds')