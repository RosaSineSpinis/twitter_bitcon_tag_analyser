from django.shortcuts import render

from datetime import datetime

from .models import HourModel, DayModel, MonthModel, Test

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from .serializer import HourSerializer, DaySerializer, MonthSerializer
from rest_framework import generics
from rest_framework import mixins
# Create your views here.


def home(request):

    objs = Test.objects.create(user_name="testName", user_surname="TestSurname")
    objs.save()

    # objs = MinutesModel.objects.all()
    #
    # for obj in objs:
    #     print(obj)
    return render(request, "home.html", {})


# generics.RetrieveAPIView
# generics.GenericAPIView
class ChartData(generics.ListAPIView, mixins.CreateModelMixin):  # (): generics.GenericAPIView
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = []
    permission_classes = []

    # lookup_field = 'pk'
    serializer_class = None
    queryset = None
    # queryset = HourModel.objects.all()
        # latest('tag_date')

    def post(self, request, *args, format=None, **kwargs):
        """
        Send data about twitter tags in post written in last ... time
        :param request: takes scopes of the data
        :return: dictionary converted to JSON
        """
        # serializer_class = HourSerializer
        dataset_kind = request.POST.get('dataset')  # name of dictionary
        print(dataset_kind)
        if dataset_kind == "hour":
            ChartData.serializer_class = HourSerializer
            ChartData.queryset = HourModel.objects.all()  # query whole database in the final version
            return self.list(request, *args, **kwargs)
        elif dataset_kind == "day":
            ChartData.serializer_class = DaySerializer
            ChartData.queryset = DayModel.objects.all()
            return self.list(request, *args, **kwargs)
        elif dataset_kind == "month":
            ChartData.serializer_class = MonthSerializer
            ChartData.queryset = MonthModel.objects.all()
            return self.list(request, *args, **kwargs)
        # return Response(queryset)  # takes dictioanry

    def get(self, request, *args, **kwargs):
        ChartData.serializer_class = HourSerializer
        ChartData.queryset = HourModel.objects.all()  # query whole database in the final version
        return self.list(request, *args, **kwargs)


    #
    # def get(self, request, format=None):
    #     print("------------------------------------------------------------------------------------GET")
    #     # dataset = MinutesModel.objects.latest('tag_date')  # query whole database in the final version
    #     # queryset = MinutesModel.objects.latest('tag_date')
    #     # print('data', dataset)
    #     # return render(request, "home.html", {})
    #     # queryset = MinutesModel.objects.latest('tag_date')
    #     # return Response(queryset)
