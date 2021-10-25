from rest_framework import serializers
from .models import HourModel, DayModel, MonthModel


class MonthSerializer(serializers.ModelSerializer):

    dictionary_tags = serializers.SerializerMethodField('_get_serialized_dict')

    def _get_serialized_dict(self, hour_object):
        _dict = getattr(hour_object, 'tag_dictionary')
        return _dict

    class Meta:
        model = HourModel
        fields = ['tag_date', 'tag_time', 'dictionary_tags']


class HourSerializer(serializers.ModelSerializer):

    dictionary_tags = serializers.SerializerMethodField('_get_serialized_dict')

    def _get_serialized_dict(self, hour_object):
        _dict = getattr(hour_object, 'tag_dictionary')
        return _dict

    class Meta:
        model = HourModel
        fields = ['tag_date', 'tag_time', 'dictionary_tags']


class DaySerializer(serializers.ModelSerializer):

    dictionary_tags = serializers.SerializerMethodField('_get_serialized_dict')

    def _get_serialized_dict(self, day_object):
        _dict = getattr(day_object, 'tag_dictionary')
        return _dict

    class Meta:
        model = DayModel
        fields = ['tag_date', 'tag_time', 'dictionary_tags', 'beginning_datetime', 'ending_datetime']
