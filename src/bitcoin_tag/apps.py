from django.apps import AppConfig
from threading import Thread
import threading
import os
import schedule
import time
from datetime import timedelta


class RunThread:

    @staticmethod
    def run_threaded(job_func):
        job_thread = threading.Thread(target=job_func)
        job_thread.start()


class StreamNewThread(Thread):

    def run(self):
        print('StreamNewThread running')
        from .twitter_stream import StreamUserClient
        from .database_operation import CreateEntryDay
        main_scheduler = schedule.Scheduler()
        print("After import")

        def fun(obj):
            print("del function works")
            del obj

        def run_stream():
            my_stream = StreamUserClient(30, main_scheduler)
            my_stream.run_stream()
            del my_stream

        # RunThread.run_threaded(run_stream)

        # schedule.every(30).seconds.do(fun, my_stream)
        # def run_threaded(job_func):
        #     job_thread = threading.Thread(target=job_func)
        #     job_thread.start()
        #
        main_scheduler.every(20).seconds.do(RunThread.run_threaded, run_stream)  # run stream
        # main_scheduler.every(60).seconds.do(RunThread.run_threaded, CreateEntryDay().create_day_entry)  # rewrite database

        # main_scheduler.every().hour.at(":01").do(RunThread.run_threaded, run_stream)  # run stream
        # main_scheduler.every().hour.at(":10").do(RunThread.run_threaded, CreateEntryDay().create_day_entry)  # rewrite database



        # schedule.every(50).seconds.do(my_stream.run_stream)
        # .minutes.do(StreamNewThread().start)
        while True:
            all_jobs = main_scheduler.get_jobs()
            print("while loop working all_jobs", all_jobs)
            main_scheduler.run_pending()
            time.sleep(1)
            for thread in threading.enumerate():
                print(thread.name)


class BitcoinTagConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bitcoin_tag'
    #own
    verbose_name = "bitcoin_tag"

    def ready(self):
        if os.environ.get('RUN_MAIN') != 'true':
            print("BitcoinTagConfig.ready works")
            # t1 = Thread(target=StreamNewThread().run)
            # for thread in enumerate():
            #     print(thread.name)
            # t1.start()
            StreamNewThread().start()
