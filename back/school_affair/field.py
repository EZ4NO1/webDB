from django.db import models
from django.core.exceptions import  ValidationError
import datetime 
start_year=1960
start_month=9
def datatonum(x):
    if len(x)!=7:
        raise ValidationError('length not 7')
        return
    a=int(x[:4])
    b=int(x[-2:])
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
def numtodate(x):
    if (not isinstance(x,tuple))or(not len(x)==2)or(not isinstance(x[0],int)) or (not isinstance(x[1],int)):
        raise ValidationError('not a tuple of 2 integer')
    a=x[0]
    b=x[1]
    if a>datetime.date.today().year:
        raise ValidationError('future')
    if a==datetime.date.today().year and b>datetime.date.today().month:
        raise ValidationError('future')
    if a<start_year:
        raise ValidationError('past')
    if a==start_year and b<start_month:
        raise ValidationError('past')
    if b<9:
        tep='0'+str(b)
    else :
        tep=str(b)
    return str(a)+'-'+tep
class YMField(models.CharField):
    description="a field of YYYY-MM type date,valid only between start_time and now"
    '''python data format:(1999,11) data_baseformat:1999-11'''
    def __init__(self,*args, **kwargs):
        super().__init__(max_length = 7)
    def from_db_value(self, value, expression, connection):
        print('from_db_value')
        return self.to_python(value)

    def to_python(self, value):
        print('to_python')
        if isinstance(value, str):
            return datatonum(value)
        if value is None:
            return value
        raise ValidationError('not None or str')
    def get_prep_value(self, value):
        if value is None:
            return value
        return numtodate(value)
class BirthField(models.DateField):
    def get_prep_value(self, value):
        print('work')
        print(value)
        print(datetime.date.today())
        if value>datetime.date.today():
            raise ValidationError('birth on future')
        return super().get_prep_value(value)