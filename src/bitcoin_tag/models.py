from django.db import models

# Create your models here.

from picklefield.fields import PickledObjectField


class YearModel(models.Model):
    tag_dictionary = PickledObjectField()
    tag_date = models.DateField(auto_now_add=False)  # date of save
    tag_time = models.TimeField(auto_now_add=False)  # time of save
    beginning_datetime = models.DateTimeField(blank=False)  # comes from MonthModel
    ending_datetime = models.DateTimeField(blank=False)  # comes from MonthModel

    def __str__(self):
        return f'{self.tag_date} {self.tag_time}'


class MonthModel(models.Model):
    tag_dictionary = PickledObjectField()
    tag_date = models.DateField(auto_now_add=True)  # date of save
    tag_time = models.TimeField(auto_now_add=True)  # time of save
    beginning_datetime = models.DateTimeField(blank=False)  # comes from HourModel the earliest object
    ending_datetime = models.DateTimeField(blank=False)  # comes from HourModel the latest object

    def __str__(self):
        return f'{self.tag_date} {self.tag_time}'


class DayModel(models.Model):
    tag_dictionary = PickledObjectField()
    tag_date = models.DateField(auto_now_add=True)  # date of save
    tag_time = models.TimeField(auto_now_add=True)  # time of save
    beginning_datetime = models.DateTimeField(blank=False)  # comes from HourModel the earliest object
    ending_datetime = models.DateTimeField(blank=False)  # comes from HourModel the latest object

    def __str__(self):
        return f'{self.tag_date} {self.tag_time}'


class HourModel(models.Model):
    tag_dictionary = PickledObjectField()  # dictionary of tags --> {#tagname: number}
    tag_date = models.DateField(auto_now_add=False)  # date of tag save
    tag_time = models.TimeField(auto_now_add=False)  # time of tag save

    def __str__(self):
        return f'{self.tag_date} {self.tag_time}'


# class MinutesModel(models.Model):
#     tag_dictionary = PickledObjectField()
#     tag_date = models.DateField(auto_now=False, auto_now_add=False, blank=False)
#     tag_time = models.TimeField(auto_now=False, auto_now_add=False)
#
#     def __str__(self):
#         return f'{self.tag_date} {self.tag_time}'


class Test(models.Model):

    user_name = models.TextField(max_length=200, default="aaa")
    user_surname = models.CharField(max_length=200, default="missing")

    def __str__(self):
        return self.user_name, self.user_surname


# class DayModel(models.Model):
#     dictionary = models.CharField(max_length=30)
#     date = models.DateField(auto_now=False, auto_now_add=False)
#     time = models.TimeField(auto_now=False, auto_now_add=False)
#
#
# class MonthModel(models.Model):
#     dictionary = models.CharField(max_length=30)
#     date = models.DateField(auto_now=False, auto_now_add=False)
#     time = models.TimeField(auto_now=False, auto_now_add=False)
