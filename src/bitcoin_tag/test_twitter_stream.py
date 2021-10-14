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
        self.number_entries = 4

    # @patch('bitcoin_tag.twitter_stream.MyStreamListener')
    @patch('bitcoin_tag.twitter_stream.tweepy.StreamListener')
    @patch('bitcoin_tag.twitter_stream.tweepy.API')
    @patch('bitcoin_tag.twitter_stream.schedule.Scheduler')
    def test_push_to_database_hour(self, MockStreamListener, mock_api, mock_scheduler):

        # mock_myStreamListener = MyStreamListener()
        MyStreamListener(mock_api, 10, mock_scheduler).push_to_database_hour()
        self.assertTrue(HourModel.objects.count(), 1)
        # api, scheduler_time, scheduler
