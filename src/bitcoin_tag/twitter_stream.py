import tweepy
import re
import sys
import time
import os
import schedule
from datetime import datetime, timedelta
from .models import HourModel, MonthModel, YearModel, DayModel  # MinutesModel
import threading
from .apps import RunThread


class AuthenticationTweepy:
    def __init__(self):
        self.consumer_key = os.environ.get('consumer_key')
        print("self.consumer_key", self.consumer_key)
        self.consumer_secret = os.environ.get('consumer_secret')
        self.access_token = os.environ.get('access_token')
        self.access_token_secret = os.environ.get('access_token_secret')
        self.bearer_token = os.environ.get('bearer_token')
        self.callback_url = ''  # some url will be here

    def authenticate(self):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret, self.callback_url)
        auth.set_access_token(self.access_token, self.access_token_secret)
        return auth

class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api, scheduler_time, scheduler):
        self.api = api
        self.me = api.me()
        self.histogram = dict()
        self.start_time = datetime.now()
        self.scheduler_time = scheduler_time
        self.stream_scheduler = scheduler
    post_counter = 0

    def on_connect(self):
        """Notify when user connected to twitter"""
        print("Connected to Twitter API!")
        print("Histogram variable on_connect", self.histogram)

        def push_to_database_hour():
            print("******************************* test is working *******************************************")
            print(self.histogram)

            obj = HourModel.objects.create(tag_dictionary=self.histogram,
                                            tag_date=datetime.now().date(),
                                            tag_time=datetime.now().time())


            self.histogram = dict()
            print("histogram state after push_to_database_hour", self.histogram)
            now = datetime.now().time()  # time object
            print("now =", now)
            # schedule.cancel_job(stream_job)

        # stream_job = schedule.every(15).seconds.do(push_to_database_hour)
        stream_job = self.stream_scheduler.every(self.scheduler_time).seconds.do(RunThread.run_threaded, push_to_database_hour).tag('stream_job')
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
    def __init__(self, time_limit, scheduler):
        self.time_limit = time_limit
        self.start_time = datetime.now()
        self.stream_scheduler = scheduler
        self.auth = AuthenticationTweepy().authenticate()
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        self.me = self.api.me()

    def run_stream(self):
        # create object of the streaming class, tweets are processed by on_status
        tweets_listener = MyStreamListener(self.api, self.time_limit, self.stream_scheduler)
        # send object to the twitter stream, send authentication and MyStreamListener class
        stream = tweepy.Stream(self.api.auth, tweets_listener)
        # filter allows us to choose proper filter which are showed, empty means everything
        stream.filter(track=['#bitcoin'], languages=["en"], is_async=True)

        # time.sleep(301)  # after time start disconnecting stream
        time.sleep(10)  # after time start disconnecting stream
        print("stream.filter end")
        self.stream_scheduler.clear('stream_job')
        stream.disconnect()

# my_stream = StreamUserCommands()
# my_stream.run_stream()

# TODO: GIT
# TODO: schedule 5min every per 1 hour and time_out 5min as a class argument
# TODO: make tests
# Finish frontend