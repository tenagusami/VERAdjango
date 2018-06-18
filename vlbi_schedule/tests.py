from django.test import TestCase

# Create your tests here.
from .models import get_new
from vlbi import utility as u


def create_test_model():
    date = u.doy2datetime(2018, 152)
    return get_new(u.decrement_day(date), date)


class ObservationTests(TestCase):

    def test_str_out(self):
        obs_model = create_test_model()[0]
        self.assertEqual(str(obs_model), obs_model.observation_ID)
