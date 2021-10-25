from django.test import TestCase
from .models import HourModel, DayModel
from .database_operation import RemoveHourEntries, RemoveDayEntries
from django.utils import timezone
import datetime
from .database_operation import CreateEntryDay
from dateutil.relativedelta import relativedelta

class HourModelTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(HourModelTestCase, cls).setUpClass()
        pass

    def setUpHourDb(self, tag_dict, tag_datetime):
        HourModel.objects.create(tag_dictionary=tag_dict,
                                 tag_date=tag_datetime.date(),
                                 tag_time=tag_datetime.time(),
                                 tag_datetime=tag_datetime)

    def setUp(self) -> None:
        print("setUp working")
        self.cutoff = 10
        self.time_list = []
        self.date_time_now = datetime.datetime.now(tz=timezone.utc)
        # minutes, hours, days, months
        self.time_interval = [[0, 0, 0, 0],  # 1
                              [10, 0, 0, 0],  # 2
                              [0, 1, 0, 0],  # 3 # hours
                              [10, 1, 0, 0],  # 4
                              [20, 1, 0, 0],  # 5
                              [0, 2, 0, 0],  # 6
                              [0, 0, 1, 0],  # 7  # days
                              [0, 1, 1, 0],  # 8
                              [0, 0, 2, 0],  # 9
                              [0, 0, 3, 0],  # 10
                              [0, 2, 3, 0],  # 11
                              [0, 0, 4, 0],  # 12
                              [0, 0, 0, 1],  # 13 # months
                              [0, 0, 1, 1],  # 14
                              [0, 0, 0, 2],  # 15
                              [0, 0, 1, 2]]  # 16

        self.number_entries = len(self.time_interval)
        for interval in self.time_interval:
            self.time_list.append(self.date_time_now
                                  - datetime.timedelta(minutes=interval[0])
                                  - datetime.timedelta(hours=interval[1])
                                  - datetime.timedelta(days=interval[2])
                                  - relativedelta(months=interval[3]))

        #
        # self.time_list.append(datetime.datetime.now(tz=timezone.utc))
        # early_date_minutes = datetime.datetime.now(tz=timezone.utc) - datetime.timedelta(minutes=self.cutoff)
        # self.time_list.append(early_date_minutes)
        #
        # # more 1hour <= x <= 2hours ago
        # early_date_minutes = datetime.datetime.now(tz=timezone.utc) \
        #                      - datetime.timedelta(hours=1)
        # self.time_list.append(early_date_minutes)
        # early_date_minutes = datetime.datetime.now(tz=timezone.utc) \
        #                      - datetime.timedelta(hours=1) \
        #                      - datetime.timedelta(minutes=10)
        # self.time_list.append(early_date_minutes)
        # early_date_minutes = datetime.datetime.now(tz=timezone.utc) \
        #                      - datetime.timedelta(hours=1) - \
        #                      datetime.timedelta(minutes=20)
        # self.time_list.append(early_date_minutes)
        #
        # # more 1day <= x < 2days ago
        # early_date_days = datetime.datetime.now(tz=timezone.utc) - datetime.timedelta(days=self.cutoff)
        # self.time_list.append(early_date_days)
        # early_date_days_1 = datetime.datetime.now(tz=timezone.utc) - datetime.timedelta(days=(self.cutoff + 1))
        # self.time_list.append(early_date_days_1)
        # early_date_days_1 = datetime.datetime.now(tz=timezone.utc) -\
        #                                           datetime.timedelta(days=(self.cutoff + 1)) + \
        #                                           datetime.timedelta(minutes=10)
        # self.time_list.append(early_date_days_1)
        #
        # # more than one month
        # early_date_month = datetime.datetime.now(tz=timezone.utc) - relativedelta(months=1)
        # self.time_list.append(early_date_month)
        # early_date_month_1 = datetime.datetime.now(tz=timezone.utc) - relativedelta(months=2)
        # self.time_list.append(early_date_month_1)
        test_tag_dict = {"#bitcoin": 1, "#eth": 2}

        for _time in self.time_list:
            self.setUpHourDb(test_tag_dict, _time)

    def tearDown(self) -> None:
        print("tearDown working")

    def create_hourmodel(self,
                         tag_dictionary={"#bitcoin": 1, "#eth": 1, "#smth": 1},
                         tag_date=datetime.datetime.now(tz=timezone.utc).date(),
                         tag_time=datetime.datetime.now(tz=timezone.utc).time(),
                         tag_datetime=datetime.datetime.now(tz=timezone.utc)):
        print("create_hourmodel")
        return HourModel.objects.create(tag_dictionary=tag_dictionary,
                                        tag_date=self.date_time_now.date(),
                                        tag_time=self.date_time_now.time(),
                                        tag_datetime=self.date_time_now)

    def test_hour_model_creation(self):
        print("test_hour_model_creation")
        e = self.create_hourmodel()
        self.assertTrue(isinstance(e, HourModel))
        self.assertTrue(isinstance(e.tag_date, datetime.date))
        self.assertTrue(isinstance(e.tag_time, datetime.time))
        self.assertTrue(isinstance(e.tag_datetime, datetime.datetime))

    def test_day_model_creation(self):
        print("test_day_model_creation")
        print("hOUR MODEL ALL", HourModel.objects.all())
        # obj = CreateEntryDay()
        # obj.create_entry()
        print("DayModel.objects.all().count()", DayModel.objects.count())
        CreateEntryDay().create_entry()
        self.assertEqual(DayModel.objects.all().count(), 1)  # check whether there is one day old dictionary in the database
        self.assertEqual(DayModel.objects.all().first().tag_dictionary, {"#bitcoin": 3, "#eth": 6})
        # there should be precisely 2 fitting entries in hourmodel


    def test_month_model_creation(self):
        print("test_month_model_creation")
    # test delete hours model with default argument
    # test delete hours model with custom argument

    # test delete day model with default argument
    # test delete day model with custom argument

    def test_delete_hour_model_default(self):
        """after cutoff time, entries should be removed"""
        self.assertEqual(HourModel.objects.count(), self.number_entries)
        RemoveHourEntries().remove_entries()
        self.assertEqual(HourModel.objects.count(), 10)

    def test_delete_hour_model_custom(self):
        """after cutoff time, entries should be removed"""
        RemoveHourEntries().remove_entries(self.date_time_now - datetime.timedelta(days=1))
        self.assertEqual(HourModel.objects.count(), 7)  # should be one removed

    def setUpDayDb(self, tag_dict, tag_datetime):
        DayModel.objects.create(tag_dictionary=tag_dict,
                                tag_date=tag_datetime.date(),
                                tag_time=tag_datetime.time(),
                                tag_datetime=tag_datetime,
                                beginning_datetime=tag_datetime,
                                ending_datetime=tag_datetime)

    def populate_day_database(self):
        # minutes, hours, days, months
        self.time_interval_day_model = [[0, 0, 1, 0],  # 1
                                        [0, 0, 5, 0],  # 2
                                        [0, 0, 10, 0],  # 3 # hours
                                        [0, 0, 15, 0],  # 4
                                        [0, 0, 30, 0],  # 5
                                        [0, 0, 31, 0],  # 6
                                        [0, 0, 0, 1],  # 7  # days
                                        [0, 0, 0, 2],  # 8
                                        [0, 0, 1, 2],  # 9
                                        [0, 0, 1, 3]]  # 10

        self.number_entries_day_model = len(self.time_interval_day_model)
        self.time_list_day_model = []
        for interval in self.time_interval_day_model:
            self.time_list_day_model.append(self.date_time_now
                                            - datetime.timedelta(minutes=interval[0])
                                            - datetime.timedelta(hours=interval[1])
                                            - datetime.timedelta(days=interval[2])
                                            - relativedelta(months=interval[3]))

        test_tag_dict = {"#bitcoin": 1, "#eth": 2}
        for _time in self.time_list_day_model:
            self.setUpDayDb(test_tag_dict, _time)

    def test_delete_day_model_default(self):
        """after cutoff time, entries should be removed"""
        self.populate_day_database()
        RemoveDayEntries().remove_entries()
        self.assertEqual(DayModel.objects.count(), 6)

    def test_delete_day_model_custom(self):
        """after cutoff time, entries should be removed"""
        self.populate_day_database()
        RemoveDayEntries().remove_entries(self.date_time_now - relativedelta(months=2))
        self.assertEqual(DayModel.objects.count(), 8)
