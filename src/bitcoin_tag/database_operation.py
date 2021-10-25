from datetime import datetime, timedelta
from .models import HourModel, MonthModel, DayModel  #YearModel, MinutesModel
from django.utils import timezone
from dateutil.relativedelta import relativedelta
import pprint

class CreateEntry:
    def __init__(self):
        print("constructor CreateEntryDay is working")
        self.histogram = {}
        self.beginning_time = None
        self.ending_time = None
        self.beginning_date = None
        self.ending_date = None
        self.objs = None
        self.beginning_datetime = None
        self.ending_datetime = None

    def create_hist(self):
        """ add instance of model to the class self.objs = Model()"""
        # change to equal date
        # objs = HourModel.objects.filter(tag_date__gte=datetime.now().date() - timedelta(days=1)).all()  # use in the
        # final version
        # objs = HourModel.objects.filter(tag_date__gte=datetime.now().date() - timedelta(minutes=3)).all() #  test 1
        # self._objs = None
        # beg_time = 0
        # end_time = 0
        if self.objs:
            print("We are in the if")
            self.beginning_datetime = self.objs.first().tag_datetime
            print("self.beginning_datetime", self.beginning_date)
            self.ending_datetime = self.objs.last().tag_datetime
            print("self.beginning_datetime", self.beginning_date)

            # self.beginning_date = self.objs.first().tag_date
            # print("self.beginning_date", self.beginning_date)
            # self.ending_date = self.objs.last().tag_date
            # print("self.ending_date", self.ending_date)
            # self.beginning_time = self.objs.first().tag_time
            # print("self.beginning_time", self.beginning_time)
            # self.ending_time = self.objs.last().tag_time
            # print("self.ending_time", self.ending_time)
            for obj in self.objs:
                for key, value in obj.tag_dictionary.items():
                    self.histogram[key] = self.histogram.get(key, 0) + value

        print("_create_hist_day eof", self.histogram,
              self.beginning_time,
              self.ending_time,
              self.beginning_date,
              self.ending_date)


        # self.beginning_date = objs.first()  # here all should have the same dates as we take 1 day
        # print("self.beginning_day = objs.first()", self.beginning_date)
        # if self.beginning_date:
        #     self.beginning_date = objs.first().tag_date
        #     print("objs.first().tag_date = objs.first().tag_date", self.beginning_date)
        # self.ending_date = objs.last()  # here all should have the same dates as we take 1 day
        # print("self.ending_day = objs.first()", self.ending_date)
        # if self.ending_date:
        #     self.ending_date = objs.last().tag_date
        #     print("self.ending_day = objs.first().tag_date", self.ending_date)
        # for obj in objs:
        #     print("obj", obj)
        #     if not beg_time or obj.tag_time < beg_time:
        #          beg_time = obj.tag_time
        #     if not end_time or obj.tag_time > end_time:
        #          end_time = obj.tag_time
        #     for key, value in obj.tag_dictionary.items():
        #         self.histogram[key] = self.histogram.get(key, 0) + value
        #     self.beginning_time = beg_time
        #     self.ending_time = end_time

    def create_entry(self):
        """overload this method"""
        pass


class CreateEntryDay(CreateEntry):

    def __init__(self):
        print("constructor CreateEntryDay is working")
        super().__init__()

    def create_hist(self):
        print("create_hist_month is working")
        self.objs = HourModel.objects.filter(tag_datetime__lte=datetime.now(tz=timezone.utc) - timedelta(hours=1))\
            .filter(tag_datetime__gt=datetime.now(tz=timezone.utc) - timedelta(hours=2))\
            .order_by('tag_datetime')

        print("objects in the scope create_hist", self.objs)
        super().create_hist()
        return self.objs

    def create_entry(self):
        self.create_hist()  # creates self.histogram
        print("self.beginning_date", self.beginning_date)
        print("self.beginning_time", self.beginning_time)
        print("self.ending_date", self.ending_date)
        print("self.ending_time",  self.ending_time)

        print("------------------------------------------------------------Day Model obj is created")
        print(timezone.localtime())
        obj = DayModel.objects.create(tag_dictionary=self.histogram,
                                      beginning_datetime=self.beginning_datetime,
                                      # (datetime.combine(self.beginning_date, self.beginning_time))
                                      ending_datetime=self.ending_datetime)
                                      # (datetime.combine(self.ending_date, self.ending_time))

        # try:
        #     print("create_day_entry obj eof", obj)
        # except ValueError:
        #     print("An ValueError exception occurred")
        # except TypeError:
        #     print("Type Error create_entry")



class CreateEntryMonth(CreateEntry):
    def create_hist(self):
        print("create_hist_month is working")
        self.objs = DayModel.objects.filter(tag_datetime__lte=datetime.now(tz=timezone.utc) - relativedelta(months=1))\
            .filter(tag_datetime__gt=datetime.now(tz=timezone.utc) - relativedelta(months=2))\
            .order_by('tag_datetime')
            # .order_by('tag_date', 'tag_time')  # test 2
        super().create_hist()
        return self.objs

    def create_entry(self):  # think about class
        objs = self.create_hist()
        print("self.beginning_date", self.beginning_date)
        print("self.beginning_time", self.beginning_time)
        print("self.ending_date", self.ending_date)
        print("self.ending_time",  self.ending_time)

        try:
            print("------------------------------------------------------------Month Model obj is created")
            obj = MonthModel.objects.create(tag_dictionary=self.histogram,
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

