from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Creations(models.Model):
	creator = models.ForeignKey(User,on_delete=models.CASCADE,related_name='creators')
	length = models.IntegerField()
	width = models.IntegerField()
	height = models.IntegerField()
	area = models.IntegerField()
	volume = models.IntegerField()
	create_date = models.DateTimeField(default=timezone.now)
	updator = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name='updators')
	up_len = models.IntegerField(blank=True,null=True)
	up_wid = models.IntegerField(blank=True,null=True)
	up_hei = models.IntegerField(blank=True,null=True)
	up_area = models.IntegerField(blank=True,null=True)
	up_vol = models.IntegerField(blank=True,null=True)
	up_date = models.DateTimeField(blank=True,null=True)

	def __str__(self):
		return f"{self.creator.username}|{self.id}"