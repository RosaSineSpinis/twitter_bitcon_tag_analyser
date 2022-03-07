from rest_framework import serializers
from .models import HourModel, DayModel, MonthModel


class MonthSerializer(serializers.ModelSerializer):

    dictionary_tags = serializers.SerializerMethodField('_get_serialized_dict')

    def _get_serialized_dict(self, hour_object):
        _dict = getattr(hour_object, 'tag_dictionary')
        return _dict

    class Meta:
        model = HourModel
        fields = ['tag_date', 'tag_time', 'dictionary_tags', 'semantic_analysis']


class HourSerializer(serializers.ModelSerializer):

    dictionary_tags = serializers.SerializerMethodField('_get_serialized_dict')
    semantic_analysis = serializers.SerializerMethodField('_get_serialized_dict_semantic_analysis')

    def _get_serialized_dict(self, hour_object):
        _dict = getattr(hour_object, 'tag_dictionary')
        return _dict

    def _get_serialized_dict_semantic_analysis(self, hour_object):
        _dict_semantic = getattr(hour_object, 'semantic_analysis')
        return _dict_semantic

    class Meta:
        model = HourModel
        fields = ['tag_date', 'tag_time', 'dictionary_tags', 'semantic_analysis']


class DaySerializer(serializers.ModelSerializer):

    dictionary_tags = serializers.SerializerMethodField('_get_serialized_dict')
    semantic_analysis = serializers.SerializerMethodField('_get_serialized_dict_semantic_analysis')

    def _get_serialized_dict(self, day_object):
        _dict = getattr(day_object, 'tag_dictionary')
        return _dict

    def _get_serialized_dict_semantic_analysis(self, day_object):
        _dict_semantic = getattr(day_object, 'semantic_analysis')
        return _dict_semantic

    class Meta:
        model = DayModel
        fields = ['tag_date', 'tag_time', 'dictionary_tags', 'beginning_datetime', 'ending_datetime', 'semantic_analysis']
