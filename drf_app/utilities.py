from .models import Box
import datetime
from django.db.models import Count, Avg

def area_vol(l,b,h):
	area = 2*(l*b+b*h+h*l)
	volume = (l*b*h)
	return area,volume

def get_average(new_area,new_vol,user,update_id):
	if update_id == None:
		old_area = Box.objects.aggregate(Avg('area'),Count('area'))
		old_vol = Box.objects.filter(creator=user).aggregate(Avg('volume'),Count('volume'))
	else:
		old_area = Box.objects.exclude(id=update_id).aggregate(Avg('area'),Count('area'))
		old_vol = Box.objects.filter(creator__username=user).exclude(id=update_id).aggregate(Avg('volume'),Count('volume'))

	area_avg = old_area['area__avg']+((new_area - old_area['area__avg']) / (old_area['area__count'] + 1))
	vol_avg = old_vol['volume__avg']+((new_vol - old_vol['volume__avg']) / (old_vol['volume__count'] + 1))
	print("\n\n\n",area_avg,vol_avg,"\n\n\n")

	if area_avg < 40 and vol_avg < 30:
		return True
	else:
		return False

def box_limit(user):
	date = datetime.date.today()
	start_week = date - datetime.timedelta(date.weekday())
	all_entries = Box.objects.filter(create_date__range=[start_week, date]).count()
	user_entries = Box.objects.filter(create_date__range=[start_week, date],creator=user).count()
	if all_entries < 10 and user_entries < 5:
		return True
	else:
		return False