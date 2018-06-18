from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView, ListView

# Create your views here.
from vlbi import utility as u
from . import forms
from . import models as m


class IndexView(TemplateView):
    template_name = 'vlbi_schedule/index.djhtml'
    model = m.Observation

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(make_default_table())
        return context


def dispatch(request):
    if request.method == 'POST':
        form = forms.QueryForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            year, doy = u.datetime2year_doy_string(date)
            return HttpResponseRedirect(
                reverse('vlbi_schedule:result', args=(year, doy)))
    return render(request, 'vlbi_schedule/index.djhtml',
                  make_default_table(
                      form=form, error_message='Invalid input!'))


class ResultView(ListView):
    template_name = 'vlbi_schedule/index.djhtml'
    model = m.Observation

    def get_queryset(self):
        pass


def result(request, year, doy):
    form = forms.QueryForm()
    date = u.doy2datetime(year, doy)
    form.fields['date'].initial = date
    result_table = {'observation_list':
                    # m.get_or_create_schedule_from_db(
                    # u.decrement_day(date),date)
                    m.get_for_daily_report(date),
                    'form': form,
                    'error_message': ''
                    }
    return render(request, 'vlbi_schedule/index.djhtml', result_table)


def make_empty_status():
    return {'observation_info': [],
            'secZ_info': [],
            }


def make_default_table(form=forms.QueryForm(), error_message=''):
    return {'observation_list': [],
            'form': form,
            'error_message': error_message
            }
