import logging
import sys
from datetime import datetime, timezone


class UTCFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        # Use datetime.fromtimestamp with timezone.utc
        ct = datetime.fromtimestamp(record.created, timezone.utc)
        if datefmt:
            # Check if '%f' is in the datefmt; if so, replace with milliseconds
            if '%f' in datefmt:
                # Get full microseconds as string (6 digits)
                micro = ct.strftime('%f')
                # Use only the first 3 digits for milliseconds
                milli = micro[:3]
                # Replace '%f' in the datefmt with the milliseconds string
                s = ct.strftime(datefmt.replace('%f', milli))
            else:
                s = ct.strftime(datefmt)
        else:
            s = ct.isoformat()
        return s


def setup_logging(logging_level=logging.INFO):
    handler = logging.StreamHandler(sys.stdout)
    formatter = UTCFormatter(
        fmt='%(asctime)s %(levelname)s %(name)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S:%M.%f'
    )
    handler.setFormatter(formatter)
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(logging_level)
