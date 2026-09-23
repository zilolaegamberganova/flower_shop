from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


scheme_view=get_schema_view(
    openapi.Info(title="FLower Shop API",default_version='v1'),
    public=True,
    permission_classes=(permissions.AllowAny,),

)

urlpatterns = [
    path('swager/',scheme_view.with_ui('swagger',cache_timeout=0),name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('', views.home_page, name='home'),
    path('dashboard/', views.main_dashboard, name='main_dashboard'),
    path('login/', views.login_page, name='login_page'),
    path('logout/', views.logout_page, name='logout_page'),
    path('products/', views.product_list, name='product_list'),
    path('products/create/', views.product_create, name='product_create'),
    path('product/<int:pk>/edit/', views.product_edit, name='edit_product'),
    path('products/delete/<int:pk>/', views.product_delete, name='product_delete'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/edit/<int:pk>/', views.category_edit, name='category_edit'),
    path('categories/delete/<int:pk>/', views.category_delete, name='category_delete'),
    path('users/', views.user_list, name='user_list'),
    path('orders/', views.order_list, name='order_list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)