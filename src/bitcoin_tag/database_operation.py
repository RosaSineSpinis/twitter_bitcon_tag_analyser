from datetime import datetime, timedelta
from .models import HourModel, MonthModel, DayModel  #YearModel, MinutesModel
from django.utils import timezone
from dateutil.relativedelta import relativedelta
import pprint

class CreateEntry:
    def __init__(self):
        print("constructor CreateEntry is working")
        self.histogram = dict()
        self.beginning_time = None
        self.ending_time = None
        self.beginning_date = None
        self.ending_date = None
        self.objs = None
        self.beginning_datetime = None
        self.ending_datetime = None
        self.hist_semantic_analysis = {-1: 0, 0: 0, 1: 0}

    def _set_objects(self):
        pass

    def _set_time_entry(self):
        if self.objs:
            print("We are in the if _set_time_entry")
            print("self.objs _set_time_entry", self.objs)
            self.beginning_datetime = self.objs.first().tag_datetime
            print("self.beginning_datetime", self.beginning_datetime)
            self.ending_datetime = self.objs.last().tag_datetime
            print("self.ending_datetime", self.ending_datetime)

    def _set_hist(self):
        """ add instance of model to the class self.objs = Model()"""
        if self.objs:
            print("We are in the if _set_hist")
            print("self.objs _set_hist", self.objs)
            for obj in self.objs:
                for key, value in obj.tag_dictionary.items():
                    self.histogram[key] = self.histogram.get(key, 0) + value

    def _set_hist_semantic_analysis(self):
        if self.objs:
            print("We are in the if _set_hist_semantic_analysis")
            print("self.objs _set_hist_semantic_analysis", self.objs)
            for obj in self.objs:
                for key, value in obj.semantic_analysis.items():
                    self.hist_semantic_analysis[key] = self.hist_semantic_analysis.get(key, 0) + value

        print("__created_histograms", self.histogram,
              self.hist_semantic_analysis,
              self.beginning_time,
              self.ending_time,
              self.beginning_date,
              self.ending_date)

    def create_entry(self):
        """overload this method"""
        pass


class CreateEntryDay(CreateEntry):

    def __init__(self):
        print("constructor CreateEntryDay is working")
        super().__init__()

    def _set_objects(self):
        self.objs = HourModel.objects.filter(tag_datetime__lte=datetime.now(tz=timezone.utc) - timedelta(days=1))\
            .filter(tag_datetime__gt=datetime.now(tz=timezone.utc) - timedelta(days=2))\
            .order_by('tag_datetime')

        print("objects in the scope CreateEntryDay", self.objs)

    # def set_hist(self):
    #     super().set_hist()
    #     return self.objs

    # def set_hist_semantic_analysis(self):
    #     pass

    def create_entry(self):
        print("create_entry function")
        self._set_objects()
        self._set_time_entry()
        self._set_hist()  # creates self.histogram
        self._set_hist_semantic_analysis()
        print("create_entry self.objs", self.objs)
        print("self.hist_semantic_analysis", self.hist_semantic_analysis)
        print("self.histogram", self.histogram)
        print("self.beginning_date", self.beginning_date)
        print("self.beginning_time", self.beginning_time)
        print("self.ending_date", self.ending_date)
        print("self.ending_time",  self.ending_time)
        print("self.beginning_datetime", self.beginning_datetime)
        print("self.ending_datetime", self.ending_datetime)

        try:
            obj = DayModel.objects.create(tag_dictionary=self.histogram,
                                          semantic_analysis=self.hist_semantic_analysis,
                                          beginning_datetime=self.beginning_datetime,
                                          # (datetime.combine(self.beginning_date, self.beginning_time))
                                          ending_datetime=self.ending_datetime)
                                          # (datetime.combine(self.ending_date, self.ending_time))
            print("------------------------------------------------------------Day Model obj was created")

        except ValueError:
            print("An ValueError exception occurred")
        except BaseException:
            print("something wrong!!! while object is created")

        # try:
        #     print("create_day_entry obj eof", obj)
        # except ValueError:
        #     print("An ValueError exception occurred")
        # except TypeError:
        #     print("Type Error create_entry")


class CreateEntryMonth(CreateEntry):

    def _set_objects(self):
        print("create_hist_month is working")
        self.objs = DayModel.objects.filter(tag_datetime__lte=datetime.now(tz=timezone.utc) - relativedelta(months=1))\
            .filter(tag_datetime__gt=datetime.now(tz=timezone.utc) - relativedelta(months=2))\
            .order_by('tag_datetime')
            # .order_by('tag_date', 'tag_time')  # test 2
        print("_set_objects - ", self.objs)
        return self.objs

    def create_entry(self):  # think about class
        self._set_objects()
        self._set_time_entry()
        self._set_hist()  # creates self.histogram
        self._set_hist_semantic_analysis()
        print("self.beginning_date", self.beginning_date)
        print("self.beginning_time", self.beginning_time)
        print("self.ending_date", self.ending_date)
        print("self.ending_time",  self.ending_time)

        try:
            print("------------------------------------------------------------Month Model obj is created")
            obj = MonthModel.objects.create(tag_dictionary=self.histogram,
                                            semantic_analysis=self._set_hist_semantic_analysis(),
                                            beginning_datetime=(datetime.combine(self.beginning_date, self.beginning_time)),
                                            ending_datetime=(datetime.combine(self.ending_date, self.ending_time)))
        except ValueError:
            print("An ValueError exception occurred")
        except BaseException:
            print("something wrong!!! while object is created")


class RemoveEntries:
    def __init__(self):
        self.cutoff_datetime = None
        # self.time = self.date_and_time.time()
        # self.date = self.date_and_time.date()

    def remove_entries(self):
        pass


class RemoveHourEntries(RemoveEntries):
    def __init__(self):
        super().__init__()
        self.cutoff_datetime = None

    def remove_entries(self, time_cutoff=datetime.now(tz=timezone.utc)-timedelta(days=3)):  # time_cutoff=timedelta(days=3)
        # self.cutoff_datetime = datetime.now(tz=timezone.utc) - time_cutoff
        self.cutoff_datetime = time_cutoff
        print("self.cutoff_datetime", self.cutoff_datetime)
        # e = HourModel.objects.filter(tag_datetime__lt=self.cutoff_datetime)
        # print("e", e, sep="\n")
        # [print(el) for el in e]
        HourModel.objects.filter(tag_datetime__lt=self.cutoff_datetime).delete()
        print("RemoveHourEntries database is working")


class RemoveDayEntries(RemoveEntries):
    """Function removes older entries than 1 month
    separate scheduler set at noon"""
    def __init__(self):
        super().__init__()
        self.cutoff_datetime = None

    def remove_entries(self, time_cutoff=datetime.now(tz=timezone.utc)-relativedelta(months=1)):
        self.cutoff_datetime = time_cutoff
        e = DayModel.objects.filter(tag_datetime__lt=self.cutoff_datetime)
        i = DayModel.objects.all()
        [print(el) for el in i]
        print("e")
        [print(el) for el in e]
        DayModel.objects.filter(tag_datetime__lt=self.cutoff_datetime).delete()
        print("RemoveDayEntries database is working")

