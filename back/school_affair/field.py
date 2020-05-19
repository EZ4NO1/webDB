from django.db import models
from django.core.exceptions import  ValidationError
import datetime 
start_year=1960
start_month=9
def datatonum(x):
    if len(x)!=7:
        raise ValidationError('length not 7')
        return
    try:
        a=int(x[:4])
        b=int(x[-2:])
    except Exception:
        raise ValidationError('not YYYY-MM format')
    if not (b>=1 and b<=12):
        raise ValidationError('not YYYY-MM format')
    if a>datetime.date.today().year:
        raise ValidationError('future')
        return
    if a==datetime.date.today().year and b>datetime.date.today().month:
        raise ValidationError('future')
        return
    if a<start_year:
        raise ValidationError('past')
        return
    if a==start_year and b<start_month:
        raise ValidationError('past')
        return
    return (a,b)
class YMField(models.CharField):
    description="a field of YYYY-MM type date,valid only between start_time and now"
    def __init__(self,*args, **kwargs):
        super().__init__(max_length = 7)
    def from_db_value(self, value, expression, connection):
        #print('from_db_value')
        return self.to_python(value)

    def to_python(self, value):
        #3print('to_python')
        if isinstance(value, str):
            datatonum(value)
            return value
        if value is None:
            return value
        raise ValidationError('not None or str')
    def get_prep_value(self, value):
        datatonum(value)
        return value

class BirthField(models.DateField):
    def get_prep_value(self, value):
        if value is None:
            return value
        #print('work')
        #print(value)
        #print(datetime.date.today())
        if value>datetime.date.today():
            raise ValidationError('birth on future')
        return super().get_prep_value(value)
    def to_python(self, value):
        a=super().to_python(value)
        if a>datetime.date.today():
            raise ValidationError('birth on future')
        return a