import datetime
from datetime import date
import dateutil
import re
import dateutil.parser as dparser



def find_date_true(text):
    try:
        match = re.search(r'\d{1,2}[/. -]\d{1,2}[/. -]\d{2,4}', text)
        return match.group()
    except:
        return None


def find_date_test_CMP1(text):
    try:
        match = re.search(r'(([\d]{1})|([\d]{2}))(/|-| |.)(([\d]{1})|([\d]{2}))(/|-| |.)(([\d]{4})|([\d]{2}))', text)
        return match.group()
    except:
        return None



def find_date_improved(text):
    try:
        match = re.search("(([3][0-1])|([1-2][0-9])|([0][1-9]))?(/|-| |.)?((([0][1-9])|[1][0-2])|("
                          "JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)|("
                          "jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec))(/|-| |.)?(([\d]{4})|[\d]{2})", text)
        return match.group()
    except:
        return None
def find_date_Improved1(text):
    try:
        match = re.search("((([3][0-1])|([1-2][0-9])|([0][1-9]))(/|-| |.))?((([0][1-9])|[1][0-2])|("
                          "JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)|("
                          "jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec))(/|-| |.)(([2][0][1-9][0-9])|([1-9]["
                          "0-9]))", text)
        return match.group()
    except:
        return None

def find_date_test(text):
    try:
        match = re.search("([0-9][0-9])(/|-| |.)([0-9][0-9])(/|-| |.)([0-9][0-9][0-9][0-9])", text)
        return match.group()
    except:
        return None


def find_date_nottested(text):
    try:
        match = re.search("(([0-9][0-9])|([0-9]))(/|\.| |-)(([0-9][0-9])|([0-9]))(/|\.| |-)(([0-9][0-9][0-9][0-9])|([0-9][0-9]))", text)
        return match.group()
    except:
        return None



    


def find_parser(text):
    try:
        if (len(text) < 6):
            return None
        else:
            match = dparser.parse(text, fuzzy=True)
            return match
    except:
        return None