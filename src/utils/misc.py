from datetime import datetime


def format_datetime(iso_timestamp):
    dt = datetime.fromisoformat(iso_timestamp.replace("Z", "+00:00"))
    return dt.strftime("%d.%m.%Y")
