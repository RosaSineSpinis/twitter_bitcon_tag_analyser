from django.test import TestCase
from .models import HourModel
from .database_operation import RemoveHourEntries
from django.utils import timezone
import datetime


class HourModelTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(HourModelTestCase, cls).setUpClass()
        pass

    def setUp(self) -> None:
        print("setUp working")
        self.cutoff = 10
        self.number_entries = 4
        early_date_minutes = datetime.datetime.now(tz=timezone.utc) - datetime.timedelta(minutes=self.cutoff)
        early_date_days = datetime.datetime.now(tz=timezone.utc) - datetime.timedelta(days=self.cutoff)
        early_date_days_1 = datetime.datetime.now(tz=timezone.utc) - datetime.timedelta(days=(self.cutoff + 1))

        HourModel.objects.create(tag_dictionary={"#bitcoin": 1, "#eth": 1, "#smth": 1},
                                 tag_date=datetime.datetime.now(tz=timezone.utc).date(),
                                 tag_time=datetime.datetime.now(tz=timezone.utc).time(),
                                 tag_datetime=datetime.datetime.now(tz=timezone.utc))

        HourModel.objects.create(tag_dictionary={"#bitcoin": 2, "#eth": 2, "#smth": 2},
                                 tag_date=early_date_minutes.date(),
                                 tag_time=early_date_minutes.time(),
                                 tag_datetime=early_date_minutes)

        HourModel.objects.create(tag_dictionary={"#bitcoin": 3, "#eth": 3, "#smth": 3},
                                 tag_date=early_date_days.date(),
                                 tag_time=early_date_days.time(),
                                 tag_datetime=early_date_days)

        HourModel.objects.create(tag_dictionary={"#bitcoin": 4, "#eth": 4, "#smth": 4},
                                 tag_date=early_date_days_1.date(),
                                 tag_time=early_date_days_1.time(),
                                 tag_datetime=early_date_days_1)

    def tearDown(self) -> None:
        print("tearDown working")

    def create_hourmodel(self,
                         tag_dictionary={"#bitcoin": 1, "#eth": 1, "#smth": 1},
                         tag_date=datetime.datetime.now(tz=timezone.utc).date(),
                         tag_time=datetime.datetime.now(tz=timezone.utc).time(),
                         tag_datetime=datetime.datetime.now(tz=timezone.utc)):
        print("create_hourmodel")
        return HourModel.objects.create(tag_dictionary=tag_dictionary,
                                        tag_date=tag_date,
                                        tag_time=tag_time,
                                        tag_datetime=tag_datetime)

    def test_hourmodel_creation(self):
        print("test_hourmodel_creation")
        e = self.create_hourmodel()
        self.assertTrue(isinstance(e, HourModel))
        self.assertTrue(isinstance(e.tag_date, datetime.date))
        self.assertTrue(isinstance(e.tag_time, datetime.time))
        self.assertTrue(isinstance(e.tag_datetime, datetime.datetime))

    def test_delete_method_1(self):
        """after cutoff time, entries should be removed"""
        self.assertEqual(HourModel.objects.count(), self.number_entries)
        RemoveHourEntries(datetime.timedelta(days=self.cutoff + 2)).remove_entries()
        self.assertEqual(HourModel.objects.count(), self.number_entries)  # should db stay untouched

    def test_delete_method_2(self):
        """after cutoff time, entries should be removed"""
        RemoveHourEntries(datetime.timedelta(days=self.cutoff + 1)).remove_entries()
        self.assertEqual(HourModel.objects.count(), self.number_entries - 1)  # should be one removed

    def test_delete_method_3(self):
        """after cutoff time, entries should be removed"""
        RemoveHourEntries(datetime.timedelta(minutes=10)).remove_entries()
        self.assertEqual(HourModel.objects.count(), self.number_entries - 3)
        # 3 entries should be removed 1 min and 2 days

        def test_delete_method_3(self):
            """after cutoff time, entries should be removed"""
            RemoveHourEntries(datetime.timedelta(minutes=0)).remove_entries()
            self.assertEqual(HourModel.objects.count(), 0)  # all entries should be removed

        # HourModel.objects.filter(tag_datetime__lte=self.cutoff_datetime).delete()
        # obj = HourModelTestCase.objects.get(id=1)
        # self.assertEqual(HourModelTestCase.objects.get(id=1), 'The lion says "roar"')
        # self.assertEqual(HourModel.objects.count(), 1)
