from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import connection
from . import forms
from . import models

# Create your views here.

def home(request):
    return render(request, 'app/home.html')

# Auth views

def signup(request):
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            password = form_data['password']
            confirm_password = form_data['confirm_password']

            if password != confirm_password:
                messages.error(request, 'Passwords do not match.')
                return render(request, 'signup.html', {'form': form})

            try:
                with connection.cursor() as cursor:
                    cursor.execute(
                        'SELECT signup(%s, %s, %s, %s, %s)',
                        [
                            form_data['first_name'],
                            form_data['last_name'],
                            form_data['phone_number'],
                            form_data['email'],
                            password,
                        ]
                    )
            except Exception as e:
                print(f"Error during signup: {e}")
                messages.error(request, 'Error during signup. Please try again.')
                return render(request, 'signup.html', {'form': form})

            messages.success(request, 'Signup successful. Please log in.')
            return redirect('login')
    else:
        form = forms.SignupForm()
    
    context = {'form': form}
    return render(request, 'app/authentication/signup.html', context=context)

def login(request):
    if request.method == 'POST':
        p_email = request.POST['email']
        p_password = request.POST['password']

        with connection.cursor() as cursor:
            cursor.callproc('user_login', [p_email, p_password])
            user_authenticated = cursor.fetchone()[0]

        if user_authenticated:
            user = authenticate(request, username=p_email, password=p_password)
            if user:
                login(request, user)
                return redirect(home)
    return render(request, 'app/authentication/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect(login)

# CRUD Actions - Suppliers Table

def list_warehouses(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM list_warehouses()')
        columns = [col[0] for col in cursor.description]
        warehouses = [dict(zip(columns, row)) for row in cursor.fetchall()]
        print(f"Warehouses: {warehouses}")

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
    return render(request, 'app/components/component_type/component-types-list.html', context=context)

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
    return render(request, 'app/components/component_type/add-component-type.html', context=context)


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
    return render(request, 'app/components/component_type/edit-component-type.html', context=context)

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

        # Aggregate stock quantity for components with the same name
        aggregated_components = {}
        for component in components:
            name = component['name']
            cursor.execute('SELECT register_stock(%s)', [name])
            stock_quantity = cursor.fetchone()[0]

            if name in aggregated_components:
                aggregated_components[name]['stock_quantity'] = stock_quantity
                aggregated_components[name]['serial_numbers'].append(component['serial_number'])
                aggregated_components[name]['purchase_dates'].append(component['purchase_date'])
                aggregated_components[name]['purchase_prices'].append(component['purchase_price'])
                aggregated_components[name]['suppliers'].append(component['supplier_name'])
            else:
                component['stock_quantity'] = stock_quantity
                component['serial_numbers'] = [component['serial_number']]
                component['purchase_dates'] = [component['purchase_date']]
                component['purchase_prices'] = [component['purchase_price']]
                component['suppliers'] = [component['supplier_name']]
                aggregated_components[name] = component

    context = {'components': list(aggregated_components.values())}
    return render(request, 'app/components/components-list.html', context=context)

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
                return redirect('ComponentsList')
            return redirect('ComponentsList')
    else:
        form = forms.ComponentForm()
    
    context = {'form': form}
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
            return redirect('ComponentsList')
    else:
        form = forms.ComponentForm(instance=component)

    context = {'form': form, 'component': component}
    return render(request, 'app/components/edit-component.html', context=context)

def delete_component(request, id):
    component = get_object_or_404(models.components, component_id=id)
    with connection.cursor() as cursor:
        cursor.execute('CALL delete_component(%s)', [id])
    return redirect(list_components)
