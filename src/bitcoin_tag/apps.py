from django.apps import AppConfig
from threading import Thread
import threading
import os
import schedule
import time
from datetime import timedelta, datetime
from django.utils import timezone
from dateutil.relativedelta import relativedelta


class RunThread:

    @staticmethod
    def run_threaded(job_func):
        job_thread = threading.Thread(target=job_func)
        job_thread.start()

class StreamNewThread(Thread):

    @staticmethod
    def migrations():
        """function created only to populate database"""
        from .models import MonthModel, DayModel, HourModel
        print("HourModel all", HourModel.objects.all())
        DayModel.objects.all()
        MonthModel.objects.all()

    def front_end_tests(self):
        """function created only for the frontend test purposes, remove at the end"""
        from .models import MonthModel, DayModel, HourModel

        HourModel.objects.create(tag_dictionary={"#btc": 3, "#eth": 4, "#ehh": 4, "#ehggg": 6, "#efff": 5, "#ehgg": 4, "#ehrr": 4, "#ehhhhh": 5, "#eh": 4, "#ehhh": 5, "#mhm": 1},
                                tag_date=(datetime.now(tz=timezone.utc) - timedelta(minutes=5)).date(),
                                tag_time=(datetime.now(tz=timezone.utc) - timedelta(minutes=5)).time(),
                                tag_datetime=(datetime.now(tz=timezone.utc) - timedelta(minutes=5)))

        HourModel.objects.create(tag_dictionary={"#btc": 4, "#eth": 8},
                                 tag_date=(datetime.now(tz=timezone.utc) - timedelta(minutes=15)).date(),
                                 tag_time=(datetime.now(tz=timezone.utc) - timedelta(minutes=15)).time(),
                                 tag_datetime=(datetime.now(tz=timezone.utc) - timedelta(minutes=15)))

        DayModel.objects.create(tag_dictionary={"#btc": 4, "#eth": 8},
                                  tag_date=(datetime.now(tz=timezone.utc) - timedelta(minutes=5)).date(),
                                  tag_time=(datetime.now(tz=timezone.utc) - timedelta(minutes=5)).time(),
                                  tag_datetime=(datetime.now(tz=timezone.utc) - timedelta(minutes=5)),
                                  beginning_datetime=datetime.now(tz=timezone.utc) - timedelta(days=6),
                                  ending_datetime=datetime.now(tz=timezone.utc) - timedelta(days=7))

        DayModel.objects.create(tag_dictionary={"#btc": 4, "#eth": 8},
                                  tag_date=(datetime.now(tz=timezone.utc) - timedelta(minutes=10)).date(),
                                  tag_time=(datetime.now(tz=timezone.utc) - timedelta(minutes=10)).time(),
                                  tag_datetime=(datetime.now(tz=timezone.utc) - timedelta(minutes=10)),
                                  beginning_datetime=datetime.now(tz=timezone.utc) - timedelta(days=7),
                                  ending_datetime=datetime.now(tz=timezone.utc) - timedelta(days=8))

        MonthModel.objects.create(tag_dictionary={"#btc": 4, "#eth": 6},
                                  tag_date=datetime.now(tz=timezone.utc).date(),
                                  tag_time=datetime.now(tz=timezone.utc).time(),
                                  tag_datetime=datetime.now(tz=timezone.utc) - relativedelta(days=1),
                                  beginning_datetime=datetime.now(tz=timezone.utc) - relativedelta(days=1),
                                  ending_datetime=datetime.now(tz=timezone.utc) - relativedelta(days=2))

        MonthModel.objects.create(tag_dictionary={"#btc": 4, "#eth": 6},
                                  tag_date=datetime.now(tz=timezone.utc).date(),
                                  tag_time=datetime.now(tz=timezone.utc).time(),
                                  tag_datetime=datetime.now(tz=timezone.utc) - relativedelta(months=2),
                                  beginning_datetime=datetime.now(tz=timezone.utc) - relativedelta(months=2),
                                  ending_datetime=datetime.now(tz=timezone.utc) - relativedelta(months=3))

        print("front end test is happening")
        print("query all ", HourModel.objects.all())

    def run(self):  # can be replaced with the constructor, otherwise start automatically

        self.main_scheduler = schedule.Scheduler()

        print('StreamNewThread running')
        from .twitter_stream import StreamUserClient
        from .database_operation import CreateEntryDay
        print("After import")


        # def run_stream():
        #     my_stream = StreamUserClient(10, main_scheduler)
        #     my_stream.run_stream()
        #     del my_stream

        '''
        #### for thest puropses only
        self.main_scheduler.every(40).seconds.do(RunThread.run_threaded, self.front_end_tests)  # run stream
        '''

        '''
        # scheduler for tests
        self.main_scheduler.every(40).seconds.do(RunThread.run_threaded, self.run_stream)  # run stream
        # self.main_scheduler.every(120).seconds.do(RunThread.run_threaded, self.day_task)  # rewrite database
        # self.main_scheduler.every(240).seconds.do(RunThread.run_threaded, self.month_task)  # rewrite database
        '''

        '''
        #### real part of the program
        self.main_scheduler.every().hour.at(":01").do(RunThread.run_threaded, self.run_stream)  # run stream
        self.main_scheduler.every().day.at("00:10").do(RunThread.run_threaded, self.day_task)  # rewrite database
        self.main_scheduler.every().day.at("00:10").do(RunThread.run_threaded, self.month_task)
        '''

        # schedule.every(50).seconds.do(my_stream.run_stream)
        # .minutes.do(StreamNewThread().start)
        # while True:
        #     all_jobs = main_scheduler.get_jobs()
        #     print("while loop working all_jobs", all_jobs)
        #     main_scheduler.run_pending()
        #     time.sleep(1)
        #     for thread in threading.enumerate():
        #         print(thread.name)
        self.scheduler_loop()

    def day_task(self):
        from .database_operation import CreateEntryDay, RemoveHourEntries
        print("day task")
        CreateEntryDay().create_entry()
        RemoveHourEntries().remove_entries()

    def month_task(self):
        from .database_operation import CreateEntryMonth, RemoveDayEntries
        print("month task")
        if datetime.today().day == 1:
            CreateEntryMonth().create_entry()
            RemoveDayEntries().remove_entries()
        return

    def run_stream(self):
        from .twitter_stream import StreamUserClient
        print("run_stream function, hour task")
        my_stream = StreamUserClient(300, self.main_scheduler)  # scheduler will work for 300 sec
        my_stream.run_stream()
        del my_stream

    def scheduler_loop(self):
        """ uncomment if you want debug """
        while True:
            all_jobs = self.main_scheduler.get_jobs()
            # print("while loop working all_jobs", all_jobs)
            # for idx, job in enumerate(all_jobs):
            #     print("idx ", idx, "job ", job)
            self.main_scheduler.run_pending()
            time.sleep(1)
            # for thread in threading.enumerate():
            #     print(thread.name)


class BitcoinTagConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bitcoin_tag'
    #own
    verbose_name = "bitcoin_tag"

    # def ready(self):
    #     # StreamNewThread().front_end_tests()  # only for test of the frontend
    #     StreamNewThread.migrations()  # to populate database

    def ready(self):
        if os.environ.get('RUN_MAIN') != 'true':
            print("BitcoinTagConfig.ready works")
    #         # StreamNewThread().front_end_tests()  # only for test of the frontend
    #
            StreamNewThread().start()
