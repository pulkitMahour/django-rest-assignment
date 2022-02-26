from django.urls import path
from django.conf.urls import url
from . import views


urlpatterns = [
	path('listall/',views.ListAll.as_view(),name='listall'),
	path('listmy/',views.ListMy.as_view(),name='listmy'),
	path('login/',views.user_login,name='login'),
	path('logout/',views.user_logout,name='logout'),
	path('add/',views.AddApi.as_view(),name='add'),
	path('update/<int:pk>/',views.UpdateApi.as_view(),name='update'),
]