from datetime import date, datetime


def validate_past_or_present(date: date):
    now = datetime.utcnow().date()
    if date > now:
        raise ValueError("%s is in the future of %s", date, now)
