from django.core.management.base import BaseCommand  # , CommandError
import vlbi_schedule.models as m
import datetime as d
from vlbi import utility as u


class Command(BaseCommand):
    help = 'Update schedule database'
    future_until_default = u.datetime_at_0h(u.get_now())+d.timedelta(days=7)
    past_from_default = u.datetime_at_0h(u.get_now())-d.timedelta(days=7)

    def add_arguments(self, parser):
        parser.add_argument('--from', type=int, nargs=2,
                            help='a year (YYYY) and a day of year (DDD)'
                            + ' for the date'
                            + ' from which data aquisition starts'
                            + ' (default = the day before 7 days from today).')
        parser.add_argument('--until', type=int, nargs=2,
                            help='a year (YYYY) and a day of year (DDD)'
                            + ' for the date'
                            + ' until which data aquisition continues'
                            + ' (default & latest ='
                            + ' the day after 7 days from today).')

    def handle(self, *args, **options):
        if options['from']:
            past_from = u.doy2datetime(*options['from'])
        else:
            past_from = self.past_from_default

        if options['until']:
            future_until = min(self.future_until_default,
                               u.doy2datetime(*options['until']))
        else:
            future_until = self.future_until_default

        m.get_or_create(past_from, future_until)
