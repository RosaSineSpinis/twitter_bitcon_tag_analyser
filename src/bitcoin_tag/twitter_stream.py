import tweepy
import re
import sys
import time
import os
import schedule
from datetime import timedelta, datetime
from .models import HourModel, MonthModel, DayModel  # YearModel, MinutesModel
import threading
from .apps import RunThread
from django.utils import timezone
from pathlib import Path
from textblob import TextBlob
import re


class TweetAnalyzer():
    """
    Functionality for analyzing and categorizing content from tweets.
    """

    def clean_tweet(self, tweet): #  removes all unnecessary signs from tweets
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def analyze_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))

        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity == 0:
            return 0
        else:
            return -1


class AuthenticationTweepy:
    BASE_SOURCE = Path(__file__).resolve().parent

    def __init__(self):
        # self.consumer_key = os.environ.get('consumer_key')
        # self.consumer_secret = os.environ.get('consumer_secret')
        # self.access_token = os.environ.get('access_token')
        # self.access_token_secret = os.environ.get('access_token_secret')
        # self.bearer_token = os.environ.get('bearer_token')
        # self.callback_url = ''  # some url will be here
        self.consumer_key = ""
        self.consumer_secret = ""
        self.access_token = ""
        self.access_token_secret = ""
        self.bearer_token = ""
        self.callback_url = ''  # some url will be here

        with open(os.path.join(AuthenticationTweepy.BASE_SOURCE, '_twitter_api_keys.py')) as f:
            while True:
                line = f.readline()
                if not line:
                    break
                line = line.strip().split()
                key_django_name = line[0].strip()
                key_django = line[2].strip("\"")
                if key_django_name == "consumer_key":
                    self.consumer_key = key_django
                elif key_django_name == "consumer_secret":
                    self.consumer_secret = key_django
                elif key_django_name == "access_token":
                    self.access_token = key_django
                elif key_django_name == "access_token_secret":
                    self.access_token_secret = key_django
                elif key_django_name == "bearer_token":
                    self.bearer_token = key_django

    def authenticate(self):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret, self.callback_url)
        auth.set_access_token(self.access_token, self.access_token_secret)
        return auth


class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api, scheduler_time, scheduler):
        self.api = api
        self.me = api.me()
        self.histogram = dict()
        self.scheduler_time = scheduler_time
        self.stream_scheduler = scheduler
        self.semantic_histogram = {0: 0, 1: 0, 2: 0}

    post_counter = 0  # static

    def push_to_database_hour(self):
        print("******************************* test is working *******************************************")
        print(self.histogram)

        obj = HourModel.objects.create(tag_dictionary=self.histogram,
                                       semantic_analysis=self.semantic_histogram,
                                       tag_date=datetime.now(tz=timezone.utc).date(),
                                       tag_time=datetime.now(tz=timezone.utc).time(),
                                       tag_datetime=datetime.now(tz=timezone.utc))

        self.histogram = dict()
        print("histogram state after push_to_database_hour", self.histogram)
        # now = datetime.now().time()  # time object
        # print("now =", now)
        # schedule.cancel_job(stream_job)

    def on_connect(self):
        """Notify when user connected to twitter"""
        print("Connected to Twitter API!")
        print("Histogram variable on_connect", self.histogram)



        # stream_job = schedule.every(15).seconds.do(push_to_database_hour)
        stream_job = self.stream_scheduler.every(self.scheduler_time).seconds.do(
            RunThread.run_threaded, self.push_to_database_hour).tag('stream_job')
        print()
        # schedule.cancel_job(stream_job)

        # .minutes.do(push_to_database_hour)

    def get_tags(self, text):
        '''return tags only'''
        tags = []  # change to set
        p = re.compile(r'#\S+')
        for word in text.split():
            m = p.match(word)
            if m:
                tags.append(word.lower().rstrip(".,?!"))  # remove interpunction
            # else:
            #     print(f'No match - {word}')
        return tags

    def make_histogram(self, hashtag_list):
        for tag in hashtag_list:
            self.histogram[tag] = self.histogram.get(tag, 0) + 1

    def on_status(self, tweet):
        if MyStreamListener.post_counter >= 100:
            print(f"post_counter, {MyStreamListener.post_counter}")
            MyStreamListener.post_counter = 0
            # print("self.histogram", self.histogram)
            # stream.disconnect()
            # return

        MyStreamListener.post_counter += 1

        #         print(f"{tweet.user.name}:{tweet.text} \n --------------------")
        tags_list = self.get_tags(tweet.text)
        # print(tags_list)
        if '#bitcoin' in tags_list:
            self.make_histogram(tags_list)  # should be done every 5 min
            # print(tweet.text)
            tweet_analyser = TweetAnalyzer()
            semantic_result = tweet_analyser.analyze_sentiment(tweet.text)
            print("semantic analyser", tweet_analyser.analyze_sentiment(tweet.text))
            # probably write code here...
            self.semantic_histogram[semantic_result] = self.semantic_histogram.get(semantic_result, 0) + 1

    def on_error(self, status):
        print("Error detected")
        return True  # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        print("Error detected")
        return True  # Don't kill the stream


    # def on_disconnect(self):
    #     if self.running is False:
    #         return
    #     self.running = False


##############Operation with client##############


class StreamUserClient:
    def __init__(self, time_scheduler, scheduler):
        self.time_scheduler = time_scheduler
        self.time_disconnect = self.time_scheduler + 10  # self.time_scheduler * 60 + 10
        self.start_time = datetime.now()
        self.stream_scheduler = scheduler
        self.auth = AuthenticationTweepy().authenticate()
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        self.me = self.api.me()

    def run_stream(self):
        print("----------------------------------------------------run stream is working")
        # create object of the streaming class, tweets are processed by on_status
        tweets_listener = MyStreamListener(self.api, self.time_scheduler, self.stream_scheduler)
        # send object to the twitter stream, send authentication and MyStreamListener class
        stream = tweepy.Stream(self.api.auth, tweets_listener)
        # filter allows us to choose proper filter which are showed, empty means everything
        stream.filter(track=['#bitcoin'], languages=["en"], is_async=True)


        # time.sleep(301)  # after time start disconnecting stream
        time.sleep(self.time_disconnect)  # after time start disconnecting stream in seconds
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^stream.filter end")
        self.stream_scheduler.clear('stream_job')
        stream.disconnect()

# my_stream = StreamUserCommands()
# my_stream.run_stream()

# Finish frontend
