from django.shortcuts import render, redirect, get_object_or_404
from . import forms
from . import models

# Create your views here.

def home(request):
    return render(request, 'app/home.html')

def list_components(request):
    component = models.components.objects.all().order_by('purchase_date')
    return render(request, 'app/components/components-list.html', {"components": component})

def create_component(request):
    if request.method == 'POST':
        form = forms.ComponentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_components)
    else:
        form = forms.ComponentForm()
    context= {'form':form}
    return render(request, 'app/components/add-components.html', context=context)

def edit_component(request, id): 
    component = get_object_or_404(models.components, component_id=id)
    if request.method == 'POST':
        form = forms.ComponentForm(request.POST, instance=component)
        if form.is_valid():
            form.save()
            return redirect(list_components)
    else:
        form = forms.ComponentForm(instance=component)
    context= {'form':form, 'component': component}
    return render(request, 'app/components/edit-component.html', context=context)

def delete_component(request, id):
    component = models.components.objects.get(component_id=id)
    try:
        component.delete()
    except:
        pass
    return redirect(list_components)