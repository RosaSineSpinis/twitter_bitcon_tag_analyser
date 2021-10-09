from django.shortcuts import render

from datetime import datetime

from .models import HourModel, DayModel, MonthModel, YearModel, Test

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from .serializer import HourSerializer, DaySerializer
from rest_framework import generics

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
class ChartData(generics.ListAPIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = []
    permission_classes = []

    # lookup_field = 'pk'
    serializer_class = HourSerializer
    queryset = HourModel.objects.all()
        # latest('tag_date')

    def post(self, request, format=None):
        """
        Send data about twitter tags in post written in last ... time
        :param request: takes scopes of the data
        :return: dictionary converted to JSON
        """

        dataset_kind = request.POST.get('dataset')  # name of dictionary
        print(dataset_kind)

        if dataset_kind == "15minutes":
            dataset = HourModel.objects.latest('tag_date')  # query whole database in the final version
        elif dataset_kind == "1day":
            pass
        elif dataset_kind == "1year":
            pass

        return Response(dataset)  # takes dictioanry



    #
    # def get(self, request, format=None):
    #     print("------------------------------------------------------------------------------------GET")
    #     # dataset = MinutesModel.objects.latest('tag_date')  # query whole database in the final version
    #     # queryset = MinutesModel.objects.latest('tag_date')
    #     # print('data', dataset)
    #     # return render(request, "home.html", {})
    #     # queryset = MinutesModel.objects.latest('tag_date')
    #     # return Response(queryset)
