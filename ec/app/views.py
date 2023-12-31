from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import auth
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.forms import ValidationError
from django.db import connection, transaction, IntegrityError
from . import forms
from . import models
import xml.etree.ElementTree as ET
from django.core.serializers import serialize
from django.core.serializers.base import SerializationError
from django.http import HttpResponse, JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@login_required(login_url="Login")
def home(request):
    return render(request, 'app/home.html')

# Auth views

def signup(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(login_view)

    context={'form': form}
    return render(request, 'app/authentication/signup.html', context=context)

def login_view(request):
    form = forms.LoginForm()
    if request.method == 'POST':
        form = forms.LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect(home)
    context = {'form': form}
    return render(request, 'app/authentication/login.html', context=context)

def logout_view(request):
    auth.logout(request)
    return redirect(login_view)

# CRUD Actions - Suppliers Table

def list_warehouses(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM list_warehouses()')
        columns = [col[0] for col in cursor.description]
        warehouses = [dict(zip(columns, row)) for row in cursor.fetchall()]

    context = {'warehouses': warehouses}
    return render(request, 'app/suppliers/warehouses/warehouses-list.html', context=context)

def create_warehouse(request):
    if request.method == 'POST':
        form = forms.WarehousesForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            try:
                with connection.cursor() as cursor:
                    cursor.execute(
                        'CALL insert_warehouse(%s, %s, %s, %s)',
                        [
                            form_data['address'],
                            form_data['city'],
                            form_data['postal_code'],
                            form_data['country'],
                        ]
                    )
            except Exception as e:
                print(request, f"Error creating warehouse: {e}")
                return redirect(list_warehouses)
            return redirect(list_warehouses)
    else:
        form = forms.WarehousesForm()
    
    context = {'form': form}
    return render(request, 'app/suppliers/warehouses/add-warehouse.html', context=context)

def edit_warehouse(request, id):
    warehouse = get_object_or_404(models.warehouse, warehouse_id=id)
    if request.method == 'POST':
        form = forms.WarehousesForm(request.POST, instance=warehouse)
        if form.is_valid():
            form_data = form.cleaned_data
            with connection.cursor() as cursor:
                cursor.execute(
                    'CALL insert_warehouse(%s, %s, %s, %s)',
                    [
                        id,
                        form_data['address'],
                        form_data['city'],
                        form_data['postal_code'],
                        form_data['country'],
                    ]
                )
            return redirect(list_warehouses)
    else:
        form = forms.WarehousesForm(instance=warehouse)

    context = {'form': form, 'warehouse': warehouse}
    return render(request, 'app/suppliers/warehouses/edit-warehouse.html', context=context)

def delete_warehouse(request, id):
    warehouse = get_object_or_404(models.warehouse, warehouse_id=id)
    with connection.cursor() as cursor:
        cursor.execute('CALL delete_warehouse(%s)', [id])
    return redirect(list_warehouses)

# CRUD Actions - Suppliers Table

def list_suppliers(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM list_suppliers()')
        columns = [col[0] for col in cursor.description]
        suppliers = [dict(zip(columns, row)) for row in cursor.fetchall()]       

    context = {'suppliers': suppliers}
    return render(request, 'app/suppliers/suppliers-list.html', context=context)

def create_supplier(request):
    if request.method == 'POST':
        form = forms.SupplierForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            try:
                with connection.cursor() as cursor:
                    warehouse_ids = form_data['warehouse'].values_list('warehouse_id', flat=True)
                    cursor.execute(
                        'CALL insert_supplier(%s, %s, %s, %s)',
                        [
                            form_data['name'],
                            form_data['phone_number'],
                            form_data['email'],
                            list(warehouse_ids),  # Convert to a list for the procedure
                        ]
                    )
            except Exception as e:
                print(request, f"Error creating supplier: {e}")
                return redirect(list_suppliers)
            return redirect(list_suppliers)
    else:
        form = forms.SupplierForm()
    
    context = {'form': form}
    return render(request, 'app/suppliers/add-supplier.html', context=context)

def edit_supplier(request, id):
    supplier = get_object_or_404(models.supplier, supplier_id=id)
    if request.method == 'POST':
        form = forms.SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form_data = form.cleaned_data
            with connection.cursor() as cursor:
                warehouse_ids = form_data['warehouse'].values_list('warehouse_id', flat=True)
                cursor.execute(
                    'CALL edit_supplier(%s, %s, %s, %s, %s)',
                    [
                        id,
                        form_data['name'],
                        form_data['phone_number'],
                        form_data['email'],
                        list(warehouse_ids),
                    ]
                )
            return redirect(list_suppliers)
    else:
        form = forms.SupplierForm(instance=supplier)

    context = {'form': form, 'supplier': supplier}
    return render(request, 'app/suppliers/edit-supplier.html', context=context)

def delete_supplier(request, id):
    supplier = get_object_or_404(models.supplier, supplier_id=id)
    with connection.cursor() as cursor:
        cursor.execute('CALL delete_supplier(%s)', [id])
    return redirect(list_suppliers)

# CRUD Actions - Component Type Table

def list_component_types(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM list_component_types()')
        columns = [col[0] for col in cursor.description]
        component_types = [dict(zip(columns, row)) for row in cursor.fetchall()]

    context = {'component_types': component_types}
    return render(request, 'app/components/component-type/component-types-list.html', context=context)

def create_component_type(request):
    if request.method == 'POST':
        form = forms.ComponentTypeForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            try:
                with connection.cursor() as cursor:
                    cursor.execute(
                        'CALL insert_component_type(%s, %s)',
                        [
                            form_data['type_name'],
                            form_data['description'],
                        ]
                    )
            except:
                # Handle integrity violation (e.g., duplicate key, unique constraint)
                # Log or handle the error appropriately
                pass
            return redirect(list_component_types)
    else:
        form = forms.ComponentTypeForm()
    
    context = {'form': form}
    return render(request, 'app/components/component-type/add-component-type.html', context=context)


def edit_component_type(request, id):
    component = get_object_or_404(models.component_type, component_type_id=id)
    if request.method == 'POST':
        form = forms.ComponentTypeForm(request.POST, instance=component)
        if form.is_valid():
            form_data = form.cleaned_data
            with connection.cursor() as cursor:
                cursor.execute(
                    'CALL edit_component_type(%s, %s, %s)',
                    [
                        id,
                        form_data['type_name'],
                        form_data['description'],
                    ]
                )
            return redirect(list_component_types)
    else:
        form = forms.ComponentTypeForm(instance=component)

    context = {'form': form, 'component': component}
    return render(request, 'app/components/component-type/edit-component-type.html', context=context)

def delete_component_type(request, id):
    component_type = get_object_or_404(models.component_type, component_type_id=id)
    with connection.cursor() as cursor:
        cursor.execute('CALL delete_component_type(%s)', [id])
    return redirect(list_component_types)

# CRUD Actions - Components Table

def list_components(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM list_components()')
        columns = [col[0] for col in cursor.description]
        components = [dict(zip(columns, row)) for row in cursor.fetchall()]

        aggregated_components = {}
        for component in components:
            name = component['name']
            type = component['component_type_id']
            key = (name, type)

            if key in aggregated_components:
                aggregated_components[key]['serial_numbers'].append(component['serial_number'])
                aggregated_components[key]['purchase_dates'].append(component['purchase_date'])
                aggregated_components[key]['purchase_prices'].append(component['purchase_price'])
                aggregated_components[key]['suppliers'].append(component['supplier_name'])
                aggregated_components[key]['edit_url'] = reverse('EditComponent', args=[component['component_id']])
                aggregated_components[key]['delete_url'] = reverse('DeleteComponent', args=[component['component_id']])
                aggregated_components[key]['stock'] += component['stock']
            else:
                component['serial_numbers'] = [component['serial_number']]
                component['purchase_dates'] = [component['purchase_date']]
                component['purchase_prices'] = [component['purchase_price']]
                component['suppliers'] = [component['supplier_name']]
                aggregated_components[key] = component

    context = {'components': list(aggregated_components.values())}
    return render(request, 'app/components/components-list.html', context=context)

def components_detail(request, name, component_type_id):
    with connection.cursor() as cursor:
        cursor.execute(
            '''SELECT 
                c.component_id,
                c.component_type_id,
                c.supplier_id,
                c.name,
                c.serial_number,
                c.purchase_date,
                c.purchase_price,
                c.image,
                s.name as supplier_name,
                ct.type_name
            FROM app_components c JOIN app_supplier s 
                ON c.supplier_id = s.supplier_id JOIN app_component_type ct 
                    ON ct.component_type_id = c.component_type_id 
            WHERE c.name = %s AND c.component_type_id = %s''', [name, component_type_id]
        )
        columns = [col[0] for col in cursor.description]
        components = [dict(zip(columns, row)) for row in cursor.fetchall()]

    context = {'components': components}
    return render(request, 'app/components/components-details.html', context=context)
    
def create_component(request):
    if request.method == 'POST':
        form = forms.ComponentForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            try:
                with connection.cursor() as cursor:
                    cursor.execute(
                        'CALL insert_component(%s, %s, %s, %s, %s, %s, %s)',
                        [
                            form_data['component_type'].component_type_id,
                            form_data['supplier'].supplier_id,
                            form_data['name'],
                            form_data['serial_number'],
                            form_data['purchase_date'],
                            form_data['purchase_price'],
                            form_data['image'],
                        ]
                    )
            except Exception as e:
                print(request, f"Error creating component: {e}")
                return redirect(list_components)
            return redirect(list_components)
    else:
        form = forms.ComponentForm()
    
    context = {'form': form}
    print(context)
    return render(request, 'app/components/add-components.html', context=context)


def edit_component(request, id):
    component = get_object_or_404(models.components, component_id=id)
    if request.method == 'POST':
        form = forms.ComponentForm(request.POST, instance=component)
        if form.is_valid():
            form_data = form.cleaned_data
            with connection.cursor() as cursor:
                cursor.execute(
                    'CALL edit_component(%s, %s, %s, %s, %s, %s, %s, %s)',
                    [
                        id,
                        form_data['component_type'].component_type_id,
                        form_data['supplier'].supplier_id,
                        form_data['name'],
                        form_data['serial_number'],
                        form_data['purchase_date'],
                        form_data['purchase_price'],
                        form_data['image'],
                    ]
                )
            with connection.cursor() as cursor:
                cursor.execute('SELECT COUNT(*) FROM app_components WHERE name = %s', [component.name])
                count = cursor.fetchone()[0]

            if count > 1:
                return redirect(components_detail, name=component.name)
            else:
                return redirect(list_components)    
    else:
        form = forms.ComponentForm(instance=component)

    context = {'form': form, 'component': component}
    return render(request, 'app/components/edit-component.html', context=context)

def delete_component(request, id):
    component = get_object_or_404(models.components, component_id=id)
    with connection.cursor() as cursor:
        cursor.execute('CALL delete_component(%s)', [id])

    with connection.cursor() as cursor:
        cursor.execute('SELECT COUNT(*) FROM app_components WHERE name = %s', [component.name])
        count = cursor.fetchone()[0]

    if count > 1:
        return redirect(components_detail, name=component.name)
    else:
        return redirect(list_components)

# CRUD Actions - Equipment Type Table

def list_equipment_types(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM list_equipment_types()')
        columns = [col[0] for col in cursor.description]
        equipment_types = [dict(zip(columns, row)) for row in cursor.fetchall()]

    context = {'equipment_types': equipment_types}
    return render(request, 'app/equipments/equipment-type/equipment-types-list.html', context=context)

def create_equipment_type(request):
    if request.method == 'POST':
        form = forms.EquipmentTypeForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            try:
                with connection.cursor() as cursor:
                    cursor.execute(
                        'CALL insert_equipment_type(%s, %s)',
                        [
                            form_data['type_name'],
                            form_data['description'],
                        ]
                    )
            except:
                # Handle integrity violation (e.g., duplicate key, unique constraint)
                # Log or handle the error appropriately
                pass
            return redirect(list_equipment_types)
    else:
        form = forms.EquipmentTypeForm()
    
    context = {'form': form}
    return render(request, 'app/equipments/equipment-type/add-equipment-type.html', context=context)

def edit_equipment_type(request, id):
    equipment_types = get_object_or_404(models.equipment_type, equipment_type_id=id)
    if request.method == 'POST':
        form = forms.EquipmentTypeForm(request.POST, instance=equipment_types)
        if form.is_valid():
            form_data = form.cleaned_data
            with connection.cursor() as cursor:
                cursor.execute(
                    'CALL edit_equipment_type(%s, %s, %s)',
                    [
                        id,
                        form_data['type_name'],
                        form_data['description'],
                    ]
                )
            return redirect(list_equipment_types)
    else:
        form = forms.EquipmentTypeForm(instance=equipment_types)

    context = {'form': form, 'equipment_types': equipment_types}
    return render(request, 'app/equipments/equipment-type/edit-equipment-type.html', context=context)

def delete_equipment_type(request, id):
    equipment_types = get_object_or_404(models.equipment_type, equipment_type_id=id)
    with connection.cursor() as cursor:
        cursor.execute('CALL delete_equipment_type(%s)', [id])
    return redirect(list_equipment_types)

# CRUD Actions - Equipments Table

def list_equipments(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM list_equipments()')
        columns = [col[0] for col in cursor.description]
        equipments = [dict(zip(columns, row)) for row in cursor.fetchall()]

        aggregated_equipments= {}
        for equipment in equipments:
            serial_number = equipment['serial_number']

            if serial_number in aggregated_equipments:
                aggregated_equipments[serial_number]['components'].append(equipment['component_name'])
            else:
                equipment['components'] = [equipment['component_name']]
                aggregated_equipments[serial_number] = equipment

    context = {'equipments': list(aggregated_equipments.values())}
    return render(request, 'app/equipments/equipments-list.html', context=context)

def create_equipment(request):
    if request.method == 'POST':
        form = forms.CreateEquipmentForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data

            with connection.cursor() as cursor:
                components_ids = form_data['components'].values_list('component_id', flat=True)
                cursor.execute(
                    'CALL insert_equipment(%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    [
                        form_data['type'].equipment_type_id, 
                        form_data['name'],
                        form_data['serial_number'],
                        form_data['value'],
                        list(components_ids),
                        form_data['production_description'],
                        form_data['production_start'],
                        form_data['production_end'],
                        form_data['labor_type'].labor_type_id,
                    ]
                )
            return redirect(list_equipments)
    else:
        form = forms.CreateEquipmentForm()

    context = {'form': form}
    return render(request, 'app/equipments/add-equipment.html', context=context)

def edit_equipment(request, id):
    equipment = get_object_or_404(models.equipments, equipment_id=id)
    if request.method == 'POST':
        form = forms.EditEquipmentForm(request.POST, instance=equipment)
        if form.is_valid():
            form_data = form.cleaned_data
            components_ids = form_data['components'].values_list('component_id', flat=True)

            with connection.cursor() as cursor:
                cursor.execute(
                    'CALL edit_equipment(%s, %s, %s, %s, %s)',
                    [
                        id,
                        form_data['name'],
                        form_data['serial_number'],
                        form_data['value'],
                        list(components_ids)
                    ]
                )
            return redirect(list_equipments)
    else:
        form = forms.EditEquipmentForm(instance=equipment)

    context = {'form': form, 'equipment': equipment}
    return render(request, 'app/equipments/edit-equipment.html', context=context)

def edit_production(request, id):
    equipment = get_object_or_404(models.production, equipment__equipment_id=id)
    if request.method == 'POST':
        form = forms.EditProductionForm(request.POST, instance=equipment)
        if form.is_valid():
            form_data = form.cleaned_data

            with connection.cursor() as cursor:
                cursor.execute(
                    'CALL edit_production(%s, %s, %s, %s, %s)',
                    [
                        id,
                        form_data['description'],
                        form_data['production_start'],
                        form_data['production_end'],
                        form_data['labor_type'].labor_type_id,
                    ]
                )
            return redirect(list_equipments)
    else:
        form = forms.EditProductionForm(instance=equipment)

    context = {'form': form, 'equipment': equipment}
    return render(request, 'app/equipments/edit-production.html', context=context)

def delete_equipment(request, id):
    equipment = get_object_or_404(models.equipments, equipment_id=id)
    with connection.cursor() as cursor:
        cursor.execute('CALL delete_equipment(%s)', [id])
    return redirect(list_equipments)

# EXPORT XML E JSON ----------------------------------------------------------------
@classmethod
def export_orders(cls, supplier_id, output_filename):
    query = f"SELECT export_orders_to_supplier({supplier_id}, '{output_filename}');"
    with connection.cursor() as cursor:
        cursor.execute(query)

def export_xml(request):
    try:
        components_data = serialize('xml', models.components.objects.all())
        response = HttpResponse(components_data, content_type='application/xml')
        response['Content-Disposition'] = 'attachment; filename="export.xml"'
        return response
    except SerializationError as e:
        return HttpResponse(f"Error during XML serialization: {e}", status=500)

# IMPORT XML E JSON ----------------------------------------------------------------
def import_xml_to_components(xml_file_path):
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    components_list = []

    for component_element in root.findall('component'):
        component_data = {
            'component_type': int(component_element.find('component_type').text),
            'supplier': int(component_element.find('supplier').text),
            'name': component_element.find('name').text,
            'serial_number': component_element.find('serial_number').text,
            'purchase_date': component_element.find('purchase_date').text,
            'purchase_price': float(component_element.find('purchase_price').text),
            'image': component_element.find('image').text if component_element.find('image') is not None else None,
        }
        components_list.append(models.components(**component_data))

    models.components.objects.bulk_create(components_list)

@csrf_exempt
def import_xml(request):
    if request.method == 'POST':
        try:
            xml_file = request.FILES['xml_file']
            import_xml_to_components(xml_file)
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

from django.db import IntegrityError, transaction

@transaction.atomic
def import_json_to_components(json_file_path):
    print("Entering import_json_to_components")
    
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    print(f"Data loaded: {data}")

    with connection.cursor() as cursor:
        try:
            cursor.execute("SELECT insert_components_from_json(%s::jsonb);", [json.dumps(data)])
            print("Query executed successfully")
            transaction.commit()
            print("Transaction committed")
        except IntegrityError as e:
            print(f"IntegrityError: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    print("Exiting import_json_to_components")


@csrf_exempt
def import_json(request):
    if request.method == 'POST':
        try:
            json_file = request.FILES['json_file']
            import_json_to_components(json_file)
            return JsonResponse({'success': True, 'message': 'Import successful'})
        except IntegrityError as e:
            print(f"IntegrityError: {e}")
            return JsonResponse({'success': False, 'error': 'Integrity error - duplicate entry', 'details': str(e)})
        except ValidationError as e:
            print(f"ValidationError: {e}")
            return JsonResponse({'success': False, 'error': 'Validation error', 'details': str(e)})
        except Exception as e:
            print(f"Exception: {e}")
            return JsonResponse({'success': False, 'error': 'An error occurred', 'details': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
