from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_view
from . import views

urlpatterns = [
    path('', views.home, name='Homepage'),
    
    #components
    path('components/', views.list_components, name='ComponentsList'),
    path('components/add', views.create_component, name='AddComponents'),
    path('components/edit/<int:id>', views.edit_component, name='EditComponent'),
    path('components/delete/<int:id>', views.delete_component, name='DeleteComponent'),
    
    #products
    path('products/', views.home, name='List-Products'),
    path('products/add', views.home, name='Add-Products'),
    path('products/update', views.home, name='Update-Products'),
    path('products/delete', views.home, name='Delete-Product'),
    
    #authentication
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)