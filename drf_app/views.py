from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.response import Response

from .serializers import CreatoionSerializers,UpdateSerializers,ListAllSerializers,LoginSerializer
from .models import Creations
from datetime import datetime
import datetime
from itertools import chain

# Create your views here.

class LoginView(generics.GenericAPIView):
	serializer_class = LoginSerializer

	def post(self, request):
		data = request.data
		username = data.get('username', '')
		password = data.get('password', '')
		user = authenticate(username=username, password=password)

		if user:
			login(request,user)

			return redirect('/')
		return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@login_required
def user_logout(request):
	logout(request)
	return redirect('/')

def area_vol(l,b,h):
	area = 2*(l*b+b*h+h*l)
	volume = (l*b*h)
	return area,volume

def box_limit(user):
	date = datetime.date.today()
	start_week = date - datetime.timedelta(date.weekday())
	end_week = start_week + datetime.timedelta(7)
	all_entries = Creations.objects.filter(create_date__range=[start_week, end_week])
	user_entries = Creations.objects.filter(create_date__range=[start_week, end_week],creator=user)
	
	if len(all_entries) < 10 and len(user_entries) < 4:
		return True
	else:
		return False

def get_average(new_area,new_vol,user):
	area_lst = list(chain(Creations.objects.all().values_list('area', flat=True),[new_area]))
	vol_lst = list(chain(Creations.objects.filter(creator=user).values_list('volume',flat=True),[new_vol]))

	area_avg = sum(area_lst)/len(area_lst)
	vol_avg = sum(vol_lst)/len(vol_lst)
	print("\n\n\n",vol_avg,area_avg,"\n\n\n")
	if area_avg < 40 and vol_avg < 27:
		return True
	else:
		return False

class AddApi(generics.CreateAPIView):
	queryset = Creations.objects.all()
	serializer_class = CreatoionSerializers
	permission_classes = [IsAdminUser]

	def create(self, request, *args,**kwargs):
		print(request.user)
		if box_limit(request.user):
			area,volume = area_vol(request.data["length"],request.data["width"],request.data["height"])
			if get_average(area,volume,request.user):
				request.data.update({'creator':request.user.id, 'area':area, 'volume':volume})
				return super(AddApi, self).create(request, *args, **kwargs)
			else:
				return Response('Average area/volume is greater then 40',status=status.HTTP_400_BAD_REQUEST)
		else:
			return Response('Box Limit is full',status=status.HTTP_400_BAD_REQUEST)
		
class UpdateApi(generics.UpdateAPIView):
	queryset = Creations.objects.all()
	serializer_class = UpdateSerializers
	permission_classes = [IsAdminUser]

	def update(self,request, *args, **kwargs):
		up_area,up_vol = area_vol(int(request.data["up_len"]),int(request.data["up_wid"]),int(request.data["up_hei"]))
		request.data.update({'updator':request.user.id,'up_area':up_area,'up_vol':up_vol,'up_date':datetime.now()})
		return super(UpdateApi, self).update(request, *args, **kwargs)


class DeleteApi(generics.DestroyAPIView):
	queryset = Creations.objects.all()
	serializer_class = UpdateSerializers
	permission_classes = [IsAdminUser]

	def destroy(self, request, *args, **kwargs):
		instance = self.get_object()
		if instance.creator == request.user:
			self.perform_destroy(instance)
			return Response(status=status.HTTP_204_NO_CONTENT)
		return Response('Only creator should delete this box',status=status.HTTP_400_BAD_REQUEST)

class ListAll(generics.ListAPIView):
	queryset = Creations.objects.all()
	serializer_class = ListAllSerializers

class ListMy(generics.ListAPIView):
	serializer_class = ListAllSerializers
	permission_classes = [IsAdminUser]

	def get_queryset(self):
		return Creations.objects.filter(creator__username=self.request.user)





