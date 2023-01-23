from datetime import datetime


def parse_date(d, format='%Y-%m-%dT%H:%M:%S'):
    return datetime.strptime(d, format)
