from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from django.core.exceptions import ValidationError
class Box(models.Model):
	creator = models.ForeignKey(User,on_delete=models.CASCADE,related_name='creators')
	length = models.IntegerField()
	width = models.IntegerField()
	height = models.IntegerField()
	area = models.IntegerField()
	volume = models.IntegerField()
	create_date = models.DateTimeField(default=timezone.now)
	up_date = models.DateTimeField(blank=True,null=True)

	def __str__(self):
		return f"{self.creator.username}|{self.id}"

	# def save(self, *args, **kwargs):
		# if self.id is None:
		
	# 	area,volume = area_vol(self.length,self.width,self.height)
	# 	if get_average(area,volume,self.creator):
	# 		self.area = area
	# 		self.volume = volume
	# 		print("\n\n\n",kwargs,self.creator,"\n\n\n")
	# 		return super(Creations,self).save(*args, **kwargs)
	# 	else:
	# 		raise ValidationError("my error message")

	# trigggers

	# post_save()




