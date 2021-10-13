from datetime import datetime, timedelta
from .models import HourModel, MonthModel, DayModel  #YearModel, MinutesModel
from django.utils import timezone

class CreateEntryDay:

    def __init__(self):
        print("constructor CreateEntryDay is working")
        self.histogram = {}
        self.beginning_time = ""
        self.ending_time = ""
        self.beginning_date = ""
        self.ending_date = ""

    def _create_hist_day(self):
        print("create_hist_month is working")
        # change to equal date
        # objs = HourModel.objects.filter(tag_date__gte=datetime.now().date() - timedelta(days=1)).all()  # use in the
        # final version
        # objs = HourModel.objects.filter(tag_date__gte=datetime.now().date() - timedelta(minutes=3)).all() #  test 1
        objs = HourModel.objects.all().order_by('tag_date', 'tag_time')  # test 2
        # beg_time = 0
        # end_time = 0
        if objs:
            self.beginning_date = objs.first().tag_date
            self.ending_date = objs.last().tag_date
            self.beginning_time = objs.first().tag_time
            self.ending_time = objs.last().tag_time
            for obj in objs:
                for key, value in obj.tag_dictionary.items():
                    self.histogram[key] = self.histogram.get(key, 0) + value

        print("_create_hist_day eof", self.histogram,
              self.beginning_time,
              self.ending_time,
              self.beginning_date,
              self.ending_date)

        return objs
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

    def create_day_entry(self):  # think about class
        objs = self._create_hist_day()
        print("self.beginning_date", self.beginning_date)
        print("self.beginning_time", self.beginning_time)
        print("self.ending_date", self.ending_date)
        print("self.ending_time",  self.ending_time)

        try:
            obj = DayModel.objects.create(tag_dictionary=self.histogram,
                                          beginning_datetime=(datetime.combine(self.beginning_date, self.beginning_time)),
                                          ending_datetime=(datetime.combine(self.ending_date, self.ending_time)))
        except ValueError:
            print("An ValueError exception occurred")
        except BaseException:
            print("something wrong!!! while object is created")

        print("create_day_entry obj eof", obj)


class RemoveEntries:
    def __init__(self, cutoff_datetime):
        self.cutoff_datetime = datetime.now(tz=timezone.utc) - cutoff_datetime
        # self.time = self.date_and_time.time()
        # self.date = self.date_and_time.date()

    def remove_entries(self):
        pass


class RemoveHourEntries(RemoveEntries):
    def __init__(self, time_cutoff):
        super().__init__(time_cutoff)

    def remove_entries(self):
        # objs = HourModel.objects.get(tag_date__exact=datetime.now().date() - timedelta(days=4)).delete()  # final version
        # objs = HourModel.objects.get(tag_time__exact=datetime.now().time() - timedelta(minutes=5)).delete()
    #     filter
        HourModel.objects.filter(tag_datetime__lte=self.cutoff_datetime).delete()
        print("remove database is working")
        # question is: change to datetime or leave date and time
        # for now I think it is better to use datetime

    # 2
    # remove older entries than x days - this scenario 3
    # separate schedule for that at noon


# def remove_month_entries():
#     pass
#     # remove older entries than x days - this scenario 3
#     # separate schedule for that at noon
#

# def create_month_entry(self):  # think about class
#     # 1
#     # schedule at noon
#     # create record
#     # push record to database
#     obj = MonthModel.objects.create(tag_dictionary=self.histogram,
#                                     tag_date=datetime.now().date(),
#                                     tag_time=datetime.now().time())
#
#
# def create_year_entry(self):
#     # schedule at noon
#     # create record
#     # push record to database
#     obj = YearModel.objects.create(tag_dictionary=self.histogram,
#                                    tag_date=datetime.now().date(),
#                                    tag_time=datetime.now().time())
#


##############Authentication##############

