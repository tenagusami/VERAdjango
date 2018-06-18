from django import forms
import datetime as d
from vlbi import utility as u


def get_current_doy():
    now = u.get_now()
    return now.toordinal() - d.date(now.year, 1, 1).toordinal() + 1


class QueryForm(forms.Form):
    date = forms.DateField(
        label='Date',
        required=True,
        initial=u.get_now(),
        widget=forms.DateInput(),
        input_formats=['%Y-%m-%d', '%Y-%j', ],
    )
