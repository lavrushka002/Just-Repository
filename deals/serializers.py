from rest_framework import serializers
from deals.models import *

class DataSerializer(serializers.ModelSerializer):
	class Meta:
		model = Data
		fields = "__all__"

class ResultSerializer(serializers.ModelSerializer):
	class Meta:
		model = ResultResponse
		fields = "__all__"