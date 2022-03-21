from django.test import TestCase
from .models import HourModel
from .database_operation import RemoveHourEntries
from django.utils import timezone
import datetime
from .twitter_stream import MyStreamListener
from unittest.mock import Mock, patch


class HourModelTestCase(TestCase):

    def setUp(self) -> None:
        print("setUp working")
        self.cutoff = 10
        self.number_entries = 4
        early_date_minutes = datetime.datetime.now(tz=timezone.utc) - datetime.timedelta(minutes=self.cutoff)

        HourModel.objects.create(tag_dictionary={"#bitcoin": 1, "#eth": 1, "#smth": 1},
                                 semantic_analysis={-1: 1, 0: 2, 1: 3},
                                 tag_date=datetime.datetime.now(tz=timezone.utc).date(),
                                 tag_time=datetime.datetime.now(tz=timezone.utc).time(),
                                 tag_datetime=datetime.datetime.now(tz=timezone.utc))

        HourModel.objects.create(tag_dictionary={"#bitcoin": 2, "#eth": 2, "#smth": 2},
                                 semantic_analysis={-1: 2, 0: 3, 1: 4},
                                 tag_date=early_date_minutes.date(),
                                 tag_time=early_date_minutes.time(),
                                 tag_datetime=early_date_minutes)

    # @patch('bitcoin_tag.twitter_stream.MyStreamListener')
    @patch('bitcoin_tag.twitter_stream.tweepy.StreamListener')
    @patch('bitcoin_tag.twitter_stream.tweepy.API')
    @patch('bitcoin_tag.twitter_stream.schedule.Scheduler')
    def test_push_to_database_hour(self, MockStreamListener, mock_api, mock_scheduler):

        # mock_myStreamListener = MyStreamListener()
        obj = MyStreamListener(mock_api, 10, mock_scheduler)
        obj.histogram = {"#bitcoin": 1, "#eth": 1}
        obj.semantic_histogram = {-1: 5, 0: 2, 1: 4}
        obj.push_to_database_hour()
        self.assertTrue(HourModel.objects.count(), 1)
