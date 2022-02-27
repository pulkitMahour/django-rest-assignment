from rest_framework import serializers
from .models import Creations
from django.contrib.auth.models import User

class CreatoionSerializers(serializers.ModelSerializer):
	creator_name = serializers.CharField(source='creator.get_full_name',read_only=True)
	class Meta:
		model = Creations
		fields = ['creator','length','width','height','area','volume','up_date','creator_name']

class UpdateSerializers(serializers.ModelSerializer):
	class Meta:
		model = Creations
		fields = ['updator','up_len','up_wid','up_hei','up_area','up_vol','up_date']

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
		model = Creations
		fields = ['length','width','height','area','volume','creator_name','up_date']

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



