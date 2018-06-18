from django.urls import path

from . import views as v

app_name = 'vlbi_schedule'
urlpatterns = [
    # path('', v.index, name='index'),
    path('', v.IndexView.as_view(), name='index'),
    path('dispatch/', v.dispatch, name='dispatch'),
    path('<int:year>/<int:doy>/result/', v.result, name='result'),
]
