from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination

from oosc.partner.models import Partner
# Create your views here.
from rest_framework import generics,status
from django.contrib.auth.models import User, Group
from oosc.partner.serializers import PartnerSerializer, PostPartnerSerializer, SavePartnerSerializer
from oosc.partner.permissions import IsAdmin
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from django_filters.rest_framework import FilterSet,DjangoFilterBackend
import django_filters
from django.db.models import Q

class NameDuplicationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = u'User already exist'

class PartnerFilter(FilterSet):
    name=django_filters.CharFilter(name="name",lookup_expr="icontains")
    class Meta:
        model=Partner
        fields=['name']


class StandardresultPagination(PageNumberPagination):
    page_size = 100
    max_page_size = 1000
    page_size_query_param = 'page_size'

class PartnerSaveFail(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = u'Error creating partner'

class ListCreatePartner(generics.ListCreateAPIView):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (DjangoFilterBackend,)
    filter_class=PartnerFilter
    pagination_class = StandardresultPagination

    def get_serializer_class(self):
        if self.request.method == "POST":
            return PostPartnerSerializer
        else:
            return PartnerSerializer
    def perform_create(self, serializer):
        username=serializer.validated_data.get("email")
        password="#partner"
        name=serializer.validated_data.get("name")
        user=""
        try:
            user=User.objects.create_user(username=username,
                                      email=username,password=password)
        except Exception as e:
            print (e.message)
            raise NameDuplicationError
        g, created = Group.objects.get_or_create(name="partners")
        # print (g,created)
        g.user_set.add(user)
        data=serializer.data
        data["user"]=user.id
        partner=SavePartnerSerializer(data=data)
        if not partner.is_valid():
            raise serializer.ValidationError(str(partner.errors))
        else:
            #
            try:
                partner.save()
            except Exception as e:
                #print (e.message,partner.validated_data)
                user.delete()
                raise PartnerSaveFail


class RetrieveUpdateDestroyPartner(generics.RetrieveUpdateDestroyAPIView):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer
    permission_classes = (IsAdmin,)