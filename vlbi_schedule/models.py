from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from vlbi import query as q
from vlbi import utility as u
import datetime as d


class Observation(models.Model):
    observation_ID = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    PI_name = models.CharField(max_length=100)
    contact_name = models.CharField(max_length=100)
    band = models.CharField(max_length=10)
    timestamp = models.IntegerField()
    comment = models.CharField(null=True, max_length=1000)

    def __str__(self):
        return self.observation_ID


def observation_list2_observation_models(observation_list):
    return [observation_info2_observation_model(obs)
            for obs in observation_list]


def observation_info2_observation_model(observation_info):
    return Observation(
        observation_ID=observation_info['observation_ID'],
        description=observation_info['description'],
        start_time=observation_info['start_time'],
        end_time=observation_info['end_time'],
        PI_name=observation_info['PI_name'],
        contact_name=observation_info['contact_name'],
        band=observation_info['band'],
        timestamp=observation_info['timestamp'],
        comment=""
    )


def get_new(date_from, date_until):
    observation_list = \
        q.get_status_synchronous(date_from, date_until)['observation_info']
    return [observation_info2_observation_model(info)
            for info in observation_list]


def get_or_create(date_from, date_until):
    new_model_list = get_new(date_from, date_until)
    db_query_set = get(date_from, date_until)
    delete_obsolete_entry(db_query_set, new_model_list)
    save_new_entry(db_query_set, new_model_list)


def delete_obsolete_entry(db_model_list, new_model_list):
    for db_model in db_model_list:
        corresponding_model = filter(
            lambda m: m.observation_ID == db_model.observation_ID,
            new_model_list)
        if not corresponding_model:
            db_model.delete()


def save_new_entry(db_query_set, new_model_list):
    for new_model in new_model_list:
        try:
            db_model = db_query_set.get(
                observation_ID=new_model.observation_ID)
        except ObjectDoesNotExist:
            try:
                new_model.save()
            except IntegrityError:
                pass
            return
        if db_model.timestamp < new_model.timestamp:
            db_model.delete()
            new_model.save()
        return


def get(date_from, date_until):
    return Observation.objects.filter(
        end_time__gte=date_from,
        start_time__lte=u.increment_day(date_until)).order_by('start_time')


def get_for_daily_report(date):
    time_delta = d.timedelta(hours=8)
    today = u.datetime_at_0h(date)
    yesterday = u.decrement_day(today)
    return get(yesterday, today).filter(
        end_time__gte=yesterday+time_delta,
        start_time__lte=today+time_delta)
