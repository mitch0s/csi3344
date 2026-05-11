from datetime import datetime
from datetime import UTC

def timestamp_now_utc():
    """
    returns ISO 8601 timestamp: e.g. "2026-05-11T04:37:21+00:00"
    """
    return datetime.now(UTC).isoformat(timespec='seconds')