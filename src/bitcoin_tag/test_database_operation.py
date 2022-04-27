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
        print("setUpClass is working")
        pass

    @classmethod
    def tearDownClass(cls):
        print("tearDownClass is working")
        super().tearDownClass()

    def _setUpHourDb(self, tag_dict, semantic_analysis, tag_datetime):
        HourModel.objects.create(tag_dictionary=tag_dict,
                                 semantic_analysis=semantic_analysis,
                                 tag_date=tag_datetime.date(),
                                 tag_time=tag_datetime.time(),
                                 tag_datetime=tag_datetime)

    def setUp(self) -> None:
        print("\n\nsetUp working")
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


        test_tag_dict = {"#bitcoin": 1, "#eth": 2}
        semantic_analysis = {-1: 5, 0: 2, 1: 4}

        for _time in self.time_list:
            self._setUpHourDb(test_tag_dict, semantic_analysis, _time)

    def tearDown(self) -> None:
        print("tearDown working")

    def create_hourmodel(self,
                         tag_dictionary={"#bitcoin": 1, "#eth": 1, "#smth": 1},
                         semantic_analysis={-1: 5, 0: 2, 1: 4},
                         tag_date=datetime.datetime.now(tz=timezone.utc).date(),
                         tag_time=datetime.datetime.now(tz=timezone.utc).time(),
                         tag_datetime=datetime.datetime.now(tz=timezone.utc)):
        print("\ncreate_hourmodel is working\n")
        return HourModel.objects.create(tag_dictionary=tag_dictionary,
                                        semantic_analysis=semantic_analysis,
                                        tag_date=self.date_time_now.date(),
                                        tag_time=self.date_time_now.time(),
                                        tag_datetime=self.date_time_now)

    def test_hour_model_creation(self):
        print("\ntest_hour_model_creation is working\n")
        e = self.create_hourmodel()
        self.assertTrue(isinstance(e, HourModel))
        self.assertTrue(isinstance(e.tag_date, datetime.date))
        self.assertTrue(isinstance(e.tag_time, datetime.time))
        self.assertTrue(isinstance(e.tag_datetime, datetime.datetime))
        self.assertEqual(HourModel.objects.all().first().semantic_analysis, {-1: 5, 0: 2, 1: 4})

    def test_day_model_creation(self):
        print("\ntest_day_model_creation is working\n")
        all_entities = HourModel.objects.all()
        for idx, entity in enumerate(all_entities):
            print("idx, ", idx, "entity", entity, "tag_dictionary", entity.tag_dictionary, "semantic_analysis", entity.semantic_analysis)
        # obj = CreateEntryDay()
        # obj.create_entry()
        print("DayModel.objects.all().count()", DayModel.objects.count())
        objs = CreateEntryDay().create_entry()
        print("objs", objs)
        self.assertEqual(DayModel.objects.all().count(), 1)  # check whether there is one day old dictionary
        # in the database
        print("DayModel value of tag_dictionary the first element", DayModel.objects.all().first().tag_dictionary)
        self.assertEqual(DayModel.objects.all().first().tag_dictionary, {"#bitcoin": 6, "#eth": 12})
        print("DayModel value of semantic the last element", DayModel.objects.all().first().semantic_analysis)
        print("DayModel value of semantic the first element", DayModel.objects.all().last().semantic_analysis)
        self.assertEqual(DayModel.objects.all().first().semantic_analysis, {-1: 30, 0: 12, 1: 24})
        # there should be precisely 2 fitting entries in hourmodel

    # def test_month_model_creation(self):
    #     print("\ntest_month_model_creation\n")

    # test delete hours model with default argument
    # test delete hours model with custom argument
    #
    # test delete day model with default argument
    # test delete day model with custom argument

    def test_delete_hour_model_default(self):
        """after cutoff time, entries should be removed"""
        print("\ntest_delete_hour_model_default is working\n")
        self.assertEqual(HourModel.objects.count(), self.number_entries)
        RemoveHourEntries().remove_entries()
        self.assertEqual(HourModel.objects.count(), 10)

    def test_delete_hour_model_custom(self):
        """after cutoff time, entries should be removed"""
        print("\ntest_delete_hour_model_custom is working\n")

        RemoveHourEntries().remove_entries(self.date_time_now - datetime.timedelta(days=1))
        self.assertEqual(HourModel.objects.count(), 7)
##########################
