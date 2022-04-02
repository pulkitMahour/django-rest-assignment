from django.shortcuts import redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.response import Response

from .serializers import CreatoionSerializers,UpdateSerializers,ListAllSerializers,LoginSerializer
from .models import Box
from django_filters import rest_framework as filters

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

class AddApi(generics.CreateAPIView):
	queryset = Box.objects.all()
	serializer_class = CreatoionSerializers
	permission_classes = [IsAdminUser]

class UpdateApi(generics.UpdateAPIView):
	queryset = Box.objects.all()
	serializer_class = UpdateSerializers
	permission_classes = [IsAdminUser]

class DeleteApi(generics.DestroyAPIView):
	queryset = Box.objects.all()
	serializer_class = UpdateSerializers
	permission_classes = [IsAdminUser]

	def destroy(self, request, *args, **kwargs):
		instance = self.get_object()
		if instance.creator == request.user:
			self.perform_destroy(instance)
			return Response(status=status.HTTP_204_NO_CONTENT)
		return Response('Only creator should delete this box',status=status.HTTP_400_BAD_REQUEST)

class ListAllFilter(filters.FilterSet):
	class Meta:
		model = Box
		fields = {'length':['gt', 'lt'], 'width':['gt', 'lt'], 'height':['gt', 'lt'], 'area':['gt', 'lt'], 'volume':['gt', 'lt'], 'creator__username':['exact'], 'up_date':['date']}

class ListAll(generics.ListAPIView):
	queryset = Box.objects.all()
	serializer_class = ListAllSerializers
	filter_backends = (filters.DjangoFilterBackend,)
	filterset_class = ListAllFilter

class ListMyFilter(filters.FilterSet):
	class Meta:
		model = Box
		fields = {'length':['gt', 'lt'], 'width':['gt', 'lt'], 'height':['gt', 'lt'], 'area':['gt', 'lt'], 'volume':['gt', 'lt']}
		
class ListMy(ListAll):
	permission_classes = [IsAdminUser]
	filterset_class = ListMyFilter

	def get_queryset(self):
		return Box.objects.filter(creator__username=self.request.user)
	
