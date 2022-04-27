from django.test import TestCase
from .models import DayModel
from .database_operation import RemoveHourEntries, RemoveDayEntries
from django.utils import timezone
import datetime
from dateutil.relativedelta import relativedelta


class DayModelTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(DayModelTestCase, cls).setUpClass()
        print("setUpClass is working")
        pass

    @classmethod
    def tearDownClass(cls):
        print("tearDownClass is working")
        super().tearDownClass()

    def setUp(self) -> None:
        print("\n\nsetUp")
        self.date_time_now = datetime.datetime.now(tz=timezone.utc)
        self.populate_day_database()

    def _setUpDayDb(self, tag_dict, semantic_analysis, tag_datetime):
        # print("\n_setUpDAYDb is working\n")
        DayModel.objects.create(tag_dictionary=tag_dict,
                                semantic_analysis=semantic_analysis,
                                tag_date=tag_datetime.date(),
                                tag_time=tag_datetime.time(),
                                tag_datetime=tag_datetime,
                                beginning_datetime=tag_datetime,
                                ending_datetime=tag_datetime)

    def populate_day_database(self):
        print("\npopulate_day_database is working\n")
        # minutes, hours, days, months
        self.time_interval_day_model = [[0, 0, 1, 0],  # 1
                                        [0, 0, 5, 0],  # 2
                                        [0, 0, 10, 0],  # 3
                                        [0, 0, 15, 0],  # 4
                                        [0, 0, 30, 0],  # 5
                                        [0, 0, 31, 0],  # 6
                                        [0, 0, 0, 1],  # 7
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
        semantic_analysis = {-1: 5, 0: 2, 1: 4}
        for _time in self.time_list_day_model:
            print("time_list_day_model", _time)
            self._setUpDayDb(test_tag_dict, semantic_analysis, _time)

        print("\ntest_day_model_creation is working\n")
        all_entities = DayModel.objects.all()
        for idx, entity in enumerate(all_entities):
            print("idx, ", idx, "entity", entity.tag_datetime, "tag_dictionary", entity.tag_dictionary, "semantic_analysis",
                  entity.semantic_analysis)

    def test_delete_day_model_default(self):
        """after cutoff time, entries should be removed"""
        RemoveDayEntries().remove_entries()
        self.assertEqual(DayModel.objects.count(), 7)

    def test_delete_day_model_custom(self):
        """after cutoff time, entries should be removed"""
        RemoveDayEntries().remove_entries(self.date_time_now - relativedelta(months=2))
        self.assertEqual(DayModel.objects.count(), 8)


