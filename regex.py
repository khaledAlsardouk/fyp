import datetime
from datetime import date
import dateutil
import re
import dateutil.parser as dparser


def find_date(text):
    try:
        match = re.search(r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}', text)
        return match.group()
    except:
        return None

def find_parser(text):
    try:
        if (len(text)<6):
            return None
        else:
            match = dparser.parse(text, fuzzy=True)
            return match
    except:
        return None
