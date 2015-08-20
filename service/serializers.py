from django.forms import widgets
from rest_framework import serializers
from .models import Case, Responder, Response
from childsos import settings

class CaseSerializer(serializers.ModelSerializer):
    reported_date = serializers.DateTimeField(format='%b %d, %Y %H:%M:%S')
    class Meta:
        model = Case

class ResponderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responder

class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response