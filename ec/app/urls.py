from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_view
from . import views

urlpatterns = [
    path('', views.home, name='Homepage'),
    
#suppliers
    path('suppliers/', views.list_suppliers, name='SuppliersList'),
    path('suppliers/add', views.create_supplier, name='AddSupplier'),
    path('suppliers/edit/<int:id>', views.edit_supplier, name='EditSupplier'),
    path('suppliers/delete/<int:id>', views.delete_supplier, name='DeleteSupplier'),
    #warehouses
        path('warehouses/', views.list_warehouses, name='WarehousesList'),
        path('warehouses/add', views.create_warehouse, name='AddWarehouse'),
        path('warehouses/edit/<int:id>', views.edit_warehouse, name='EditWarehouse'),
        path('warehouses/delete/<int:id>', views.delete_warehouse, name='DeleteWarehouse'),

#components
    path('components/', views.list_components, name='ComponentsList'),
    path('components/add', views.create_component, name='AddComponent'),
    path('components/edit/<int:id>', views.edit_component, name='EditComponent'),
    path('components/delete/<int:id>', views.delete_component, name='DeleteComponent'),
    #component types
        path('component-types/', views.list_component_types, name='ComponentTypesList'),
        path('component-types/add', views.create_component_type, name='AddComponentType'),
        path('component-types/edit/<int:id>', views.edit_component_type, name='EditComponentType'),
        path('component-types/delete/<int:id>', views.delete_component_type, name='DeleteComponentType'),
    
    #products
    path('products/', views.home, name='ListProducts'),
    path('products/add', views.home, name='AddProducts'),
    path('products/edit/<int:id>', views.home, name='EditProduct'),
    path('products/delete/<int:id>', views.home, name='DeleteProduct'),
    
    #authentication
    path('signup/', views.home, name='Signup'),
    path('login/', views.home, name='Login'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)