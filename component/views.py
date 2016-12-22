
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Component
from .forms import ComponentForm
from django.contrib.auth.decorators import login_required



@login_required
def list(request):
    components = Component.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'component/list.html', {'components':components})


@login_required
def new(request):
    if request.method == "POST":
        form = ComponentForm(request.POST)
        if form.is_valid():
            _name = form.cleaned_data['name']
            _description = form.cleaned_data['description']
            _author=request.user          
            _created_date = timezone.now()
            _modified_date = timezone.now()
            _published_date = timezone.now()
            _inlet_ports=form.cleaned_data['inlet_ports']
            #_outlet_ports=form.cleaned_data['outlet_ports']
            _function=form.cleaned_data['function']
            _jacobian=form.cleaned_data['jacobian']

            component=Component(name=_name,
                                description=_description,
                                author=_author,
                                created_date=_created_date,
                                modified_date=_modified_date,
                                published_date=_published_date,
                                inlet_ports=_inlet_ports,
                                #outlet_ports=_outlet_ports,
                                function=_function,
                                jacobian=_jacobian,
                                ) 
            component.save()
            return redirect('component:list')
    else:
        form = ComponentForm()

    return render(request, 'component/edit.html', {'form': form})

@login_required
def edit(request,pk):

    component = get_object_or_404(Component, pk=pk)

    if request.method == "POST":
        form = ComponentForm(request.POST)

        if form.is_valid():
            _name = form.cleaned_data['name']
            _description = form.cleaned_data['description']
            _author=request.user          
            _created_date = timezone.now()
            _modified_date = timezone.now()
            _published_date = timezone.now()
            _inlet_ports=form.cleaned_data['inlet_ports']
            #_outlet_ports=form.cleaned_data['outlet_ports']
            _function=form.cleaned_data['function']
            _jacobian=form.cleaned_data['jacobian']

            component.name=_name
            component.description=_description
            component.author=_author
            component.created_date=_created_date
            component.modified_date=_modified_date
            component.published_date=_published_date
            component.inlet_ports=_inlet_ports
            #component.outlet_ports=_outlet_ports
            component.function=_function
            component.jacobian=_jacobian
                               
            component.save()
            return redirect('component:list')
    else:
        context={'name':component.name,
                 'description':component.description,
                 'author':component.author,
                 'created_date':component.created_date,
                 'modified_date':component.modified_date,
                 'published_date':component.published_date,
                 'inlet_ports':component.inlet_ports,
                 #'outlet_ports':component.inlet_ports,
                 'function':component.function,
                 'jacobian':component.jacobian,
                }
        form = ComponentForm(context)

    return render(request, 'component/edit.html', {'form': form})

@login_required
def delete(request,pk):

    component = get_object_or_404(Component, pk=pk)

    component.delete()       

    return redirect('component:list')

