from django.forms import widgets
from rest_framework import serializers
from .models import Case, Responder, Response, CaseResponse
from childsos import settings

class CaseSerializer(serializers.ModelSerializer):
    reported_date = serializers.DateTimeField(format='%b %d, %Y %H:%M:%S')
    case_responses = serializers.StringRelatedField(many=True, allow_null=True, required=False)
    class Meta:
        model = Case

class ResponderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responder

class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response

class CaseResponseSerializer(serializers.ModelSerializer):
    responded_date = serializers.DateTimeField(format='%b %d, %Y %H:%M:%S')
    class Meta:
        model = CaseResponse