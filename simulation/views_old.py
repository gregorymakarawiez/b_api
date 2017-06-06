
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Simulation
from .forms import  SimulationForm
from django.contrib.auth.decorators import login_required


@login_required
def list(request):
    simulations = Simulation.objects.order_by('published_date')
    return render(request, 'simulation/list.html', {'simulations':simulations})

@login_required
def new(request):
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
    return render(request, 'simulation/edit.html', {'form': form, 'templates':templates, 'steps':steps})


@login_required
def edit(request,pk):  

    simulation = get_object_or_404(Simulation, pk=pk)

    if request.method == "POST":
        form = SimulationForm(request.POST)

        if form.is_valid():
            cleaned_data=form.cleaned_data
            cleaned_data.update({
                'author':request.user,
                'created_date': timezone.now(),
                'modified_date': timezone.now(),
                'published_date': timezone.now()})
            for key in cleaned_data:
                setattr(simulation, key, cleaned_data[key])
 
            simulation.save()
            return redirect('simulation:list')
    else:
        context=get_context(simulation)
        print(context)
        form = SimulationForm(context)

        templates=['simulation/edit1.html','simulation/edit2.html','simulation/edit3.html']
        steps=['About','Inlet Data','Outlet Data']
    return render(request, 'simulation/edit.html', {'form': form, 'templates':templates, 'steps':steps})

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





