from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from walks.views import get_orders, create_order

schema_view = get_schema_view(
   openapi.Info(
      title="Dog Walking Service API",
      default_version='v1',
      description="API documentation for Dog Walking Service",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('walks.urls')),
    path('api/orders/<str:date>/', get_orders, name='get_orders'),
    path('api/order/', create_order, name='create_order'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]