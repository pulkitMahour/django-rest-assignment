from rest_framework import serializers
from .models import Box
from django.contrib.auth.models import User
from .utilities import area_vol, get_average, box_limit
import datetime

class CreatoionSerializers(serializers.ModelSerializer):
	creator = serializers.CharField(source='creator.username')

	class Meta:
		model = Box
		fields = ['id','creator','length','width','height']

	def create(self, validated_data):
		user = self.context['request'].user
		if box_limit(user):
			area,volume = area_vol(validated_data['length'],validated_data['width'],validated_data['height'])
			if get_average(area,volume,user,None):
				validated_data.update({'creator':user, 'area':area, 'volume':volume})
				return super().create(validated_data)
			else:
				raise serializers.ValidationError("Average area/volume is greater then 40")
		else:
			raise serializers.ValidationError("Box Limit is full")

class UpdateSerializers(serializers.ModelSerializer):
	class Meta:
		model = Box
		fields = ['length','width','height']

	def update(self, instance, validated_data):
		area,volume = area_vol(validated_data['length'],validated_data['width'],validated_data['height'])
		if get_average(area,volume,instance.creator.username,instance.id):
			validated_data.update({'area':area, 'volume':volume, 'up_date':datetime.datetime.now()})
			return super().update(instance, validated_data)
		else:
			raise serializers.ValidationError("Average area/volume is greater then 40")

class MethodField(serializers.SerializerMethodField):
	def __init__(self, method_name=None, **kwargs):
		super().__init__(method_name) 
		self.func_kwargs = kwargs

	def to_representation(self, value):
		method = getattr(self.parent, self.method_name)
		return method(value, **self.func_kwargs)

class ListAllSerializers(serializers.ModelSerializer):
	creator_name = MethodField('is_staff_user',types="name")
	up_date = MethodField('is_staff_user',types="date")

	class Meta:
		model = Box
		fields = ['id','length','width','height','area','volume','creator_name','up_date']

	def is_staff_user(self, obj, types=""):
		user = self.context['request'].user
		if user.is_staff and types=="name":
			return obj.creator.get_full_name()
		elif user.is_staff and types=="date":
			return obj.up_date
		else:
			return "Only available for staff users"

class LoginSerializer(serializers.ModelSerializer):
	password = serializers.CharField(max_length=65, min_length=8, write_only=True, style={'input_type': 'password', 'placeholder': 'Password'})
	username = serializers.CharField(max_length=255, min_length=2)

	class Meta:
		model = User
		fields = ['username', 'password']



