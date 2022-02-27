from django.urls import path, path
from . import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
	openapi.Info(
		title="rest API",
		default_version='v1',
		description="CRUD request",
	),
	public=True,
	permission_classes=[permissions.AllowAny],
)

urlpatterns = [
	path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
	path('listall/',views.ListAll.as_view(),name='listall'),
	path('listmy/',views.ListMy.as_view(),name='listmy'),
	path('accounts/login/',views.LoginView.as_view(),name='login'),
	path('accounts/logout/',views.user_logout,name='logout'),
	path('add/',views.AddApi.as_view(),name='add'),
	path('update/<int:pk>/',views.UpdateApi.as_view(),name='update'),
	path('delete/<int:pk>/',views.DeleteApi.as_view(),name='delete'),
]

