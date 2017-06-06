
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Simulation
from .forms import  SimulationForm
from django.contrib.auth.decorators import login_required
from component.models import Component
from component.views import make_form
from django.core.urlresolvers import resolve

import json

@login_required
def list(request):
    simulations = Simulation.objects.order_by('published_date')
    return render(request, 'simulation/list.html', {'simulations':simulations})


@login_required
def new_old(request):

    components=Component.objects.all()
    inlet_ports,outlet_ports=get_ports(components)

    if request.method == "POST":
        form = SimulationForm(request.POST)
        if form.is_valid():
            cleaned_data=form.cleaned_data
            cleaned_data.update({
                'author':request.user,
                'created_date': timezone.now(),
                'modified_date': timezone.now(),
                'published_date': timezone.now()})
            simulation=Simulation(**cleaned_data) 
            simulation.save()
            return redirect('simulation:list')
    else:
        form = SimulationForm()
        templates=['simulation/edit1.html','simulation/edit2.html','simulation/edit3.html']
        steps=['About','Inlet Data','Outlet Data']
    return render(request, 'simulation/edit.html', {'form': form, 'templates':templates, 'steps':steps, 'inlet_ports':inlet_ports, 'outlet_ports':outlet_ports})



@login_required
def new_details(request):  

    if request.method == "POST":
        print("edit_details:POST")
        form = SimulationForm(request.POST)

        if form.is_valid():
            cleaned_data=form.cleaned_data
            cleaned_data.update({
                'author':request.user,
                'modified_date': timezone.now(),
                'published_date': timezone.now()})

            simulation=Simulation()

            for key in cleaned_data:
                setattr(simulation, key, cleaned_data[key])
 
            simulation.save()

            if request.POST.get("to_list"):
                return redirect("simulation:list")
            elif request.POST.get("to_edit_data"):  
                return redirect("simulation:edit_data", simulation.pk)
    else:
        form = SimulationForm()

    return render(request, 'simulation/edit_details.html', {'form': form})


@login_required
def edit_details(request,pk):  

    simulation = get_object_or_404(Simulation, pk=pk)
    components=Component.objects.all()

    if request.method == "POST":
        print("edit_details:POST")
        form = SimulationForm(request.POST)

        if form.is_valid():
            cleaned_data=form.cleaned_data
            cleaned_data.update({
                'author':request.user,
                'modified_date': timezone.now(),
                'published_date': timezone.now()})
            # if component has been changed, reset inlet/outlet data data
            if cleaned_data['component'] != simulation.component:
                simulation.inlet_data={}
                simulation.outlet_data={}

            #for key in cleaned_data:
                #setattr(simulation, key, cleaned_data[key])
            simulation.name=cleaned_data['name']
            simulation.description=cleaned_data['description']
            simulation.component=cleaned_data['component']
 
            simulation.save()

            if request.POST.get("to_list"):
                return redirect("simulation:list")
            elif request.POST.get("to_edit_data"):  
                return redirect("simulation:edit_data", simulation.pk)

    else:
        print("edit_details:GET")
        context=get_context(simulation)
        print(context)
        form = SimulationForm(context)

    return render(request, 'simulation/edit_details.html', {'form': form})



@login_required
def edit_data(request,pk):

    simulation = get_object_or_404(Simulation, pk=pk)
    component=simulation.component

    try: 
        inlet_ports = json.loads(component.inlet_ports)
    except ValueError as error:
        raise ValueError("Error in edit_data: invalid json")
    try: 
        print(simulation.inlet_data)
        inlet_data = json.loads(simulation.inlet_data)
    except ValueError as error:
        inlet_data={}
    print(inlet_ports)
    print(inlet_data)

    InletForm=make_form(inlet_ports,prefix="inlet", values=inlet_data)

    if request.method == "POST":
        inlet_form=InletForm(request.POST)
        print("Submit")
        if inlet_form.is_valid(): 
            print(inlet_form.cleaned_data)
            try: 
                simulation.inlet_data = json.dumps(inlet_form.cleaned_data)
                simulation.save()
            except ValueError as error:
                raise ValueError("Error in edit_data: invalid json")             

            if request.POST.get("to_edit_details"):
                return redirect("simulation:edit_details", simulation.pk)
            elif request.POST.get("to_view_results"): 
                simulate(pk) 
                return redirect("simulation:view_results", simulation.pk)
            elif request.POST.get("to_list"):  
                return redirect("simulation:list")
   
    return render(request, 'simulation/edit_data.html', {'form': InletForm, 'ports':inlet_ports,'prefix':'inlet'})


@login_required
def view_results(request,pk):

    simulation = get_object_or_404(Simulation, pk=pk)
    component=simulation.component

    try: 
        outlet_ports = json.loads(component.outlet_ports)
    except ValueError as error:
        raise ValueError("Error in view_results: invalid json")
    try: 
        print(simulation.outlet_data)
        outlet_data = json.loads(simulation.outlet_data)
    except ValueError as error:
        outlet_data={}
    print(outlet_ports)
    print(outlet_data)

    OutletForm=make_form(outlet_ports,prefix="outlet", values=outlet_data)

    if request.method == "POST":
        outlet_form=OutletForm(request.POST)
        print("Submit")
        if outlet_form.is_valid(): 
            #print(outlet_form.cleaned_data)
            #try: 
            #    simulation.outlet_form = json.dumps(outlet_form.cleaned_data)
            #    simulation.save()
            #except ValueError as error:
            #    raise ValueError("Error in view_results: invalid json")             

            if request.POST.get("to_edit_data"):
                return redirect("simulation:edit_data", simulation.pk)
            elif request.POST.get("to_list"):  
                return redirect("simulation:list")
   
    return render(request, 'simulation/view_results.html', {'form': OutletForm, 'ports':outlet_ports,'prefix':'outlet'})


@login_required
def delete(request,pk):

    simulation = get_object_or_404(Simulation, pk=pk)

    simulation.delete()       

    return redirect('simulation:list')


def get_context(o):
# Prepare context for edit view
    context={}
    for field in o._meta.get_fields():
        field_name=field.name
        field_type=field.get_internal_type()
        # remove Autofields
        if field_type is not 'AutoField':
            field_value=getattr(o,field_name)
            context[field_name]=field_value
    return context

def get_ports(components):
    inlet_ports={}
    outlet_ports={}
    for component in components:
        inlet_ports[component.name]=component.inlet_ports
        outlet_ports[component.name]=component.outlet_ports

    try:
        inlet_ports=json.dump(inlet_ports)
        outlet_ports=json.dump(outlet_ports)
    except TypeError:
        print("Error in 'get_ports': Unable to serialize the object")

    return (inlet_ports,outlet_ports)


def simulate(pk):
    pass



