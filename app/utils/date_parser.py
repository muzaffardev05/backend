
from datetime import date, timedelta
from dateutil.parser import parse
class DateParser:

    @staticmethod
    def today():
        today=date.today()
        return today, today
    
    @staticmethod
    def yesterday():
        d=date.today()-timedelta(days=1)
        return d, d
    @staticmethod
    def tomorrow():
        d=date.today()+timedelta(days=1)
        return d, d
    
    @staticmethod
    def this_week():
        today=date.today()
        start=today-timedelta(days=today.weekday())
        end=start+timedelta(days=6)
        return start,end
    
    @staticmethod
    def last_week():
        today=date.today()
        end=today-timedelta(days=today.weekday()+1)
        start=end-timedelta(days=6)
        return start,end
    
    @staticmethod
    def this_month():
        today=date.today()
        start=today.replace(day=1)
        if today.month==12:
            end=date(today.year+1,1,1)-timedelta(days=1)
        else:
            end=date(today.year,today.month+1,1)-timedelta(days=1)    

        return start,end    
    

    @staticmethod
    def parse_date(text):
        try:
            d=parse(text,fuzzy=True).date()
            return d
        except Exception:
            return None