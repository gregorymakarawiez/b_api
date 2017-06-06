
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Component
from .forms import ComponentForm
from django.contrib.auth.decorators import login_required
from django.db.models.signals import pre_save
from django.dispatch import receiver
import json
from django import forms
from form_utils.forms import BetterForm

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
            _outlet_ports=form.cleaned_data['outlet_ports']
            _function=form.cleaned_data['function']
            _jacobian=form.cleaned_data['jacobian']

            component=Component(name=_name,
                                description=_description,
                                author=_author,
                                created_date=_created_date,
                                modified_date=_modified_date,
                                published_date=_published_date,
                                inlet_ports=_inlet_ports,
                                outlet_ports=_outlet_ports,
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
            _outlet_ports=form.cleaned_data['outlet_ports']
            _function=form.cleaned_data['function']
            _jacobian=form.cleaned_data['jacobian']

            component.name=_name
            component.description=_description
            component.author=_author
            component.created_date=_created_date
            component.modified_date=_modified_date
            component.published_date=_published_date
            component.inlet_ports=_inlet_ports
            component.outlet_ports=_outlet_ports
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
                 'outlet_ports':component.outlet_ports,
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



@login_required
def form_preview(request,pk):

    component = get_object_or_404(Component, pk=pk)

    try: 
        inlet_ports = json.loads(component.inlet_ports)
    except ValueError as error:
        raise ValueError("Error in form_preview: invalid json")
    try: 
        inlet_data = json.loads(component.inlet_data)
        print("preparing inlet_data for GET...")
        print(component.inlet_data)
    except ValueError as error:
        inlet_data={}

    InletForm=make_form(inlet_ports,prefix="inlet", values=inlet_data)
    #component.inlet_form=inlet_form({}).as_table()

    if request.method == "POST":
        inlet_form=InletForm(request.POST)
        print("Submit")
        if inlet_form.is_valid(): 
            print(inlet_form.cleaned_data)
            try: 
                component.inlet_data = json.dumps(inlet_form.cleaned_data)
                print("Saving inlet_data")
                print(component.inlet_data)
                component.save()
            except ValueError as error:
                raise ValueError("Error in form_preview: invalid json")
             

        return redirect('component:list')


    return render(request, 'component/form_preview.html', {'form': InletForm, 'ports':inlet_ports,'prefix':'inlet'})





@login_required
def form_preview_old(request,pk):

    component = get_object_or_404(Component, pk=pk)

    try: 
        inlet_ports = json.loads(component.inlet_ports)
    except ValueError as error:
        raise ParseError("Error in form_preview: invalid json")

    inlet_form=make_form(inlet_ports,prefix="inlet")
    component.inlet_form=inlet_form({}).as_table()

    if request.method == "POST":
        return redirect('component:list')

    return render(request, 'component/form_preview.html', {'form': inlet_form, 'ports':inlet_ports})


#@receiver(pre_save, sender=Component)
def form_builder(sender, instance, **kwargs):
    print("<<<<<<< form_builder >>>>>>>>>>>")

    try: 
        inlet_ports = json.loads(instance.inlet_ports)
    except ValueError as error:
        raise ParseError("Error in form_builder: invalid json")

    data=inlet_ports["data"]
    structure=inlet_ports["structure"]

    form=make_form(data, structure)
    instance.inlet_form=form({}).as_table()




def make_form(ports, prefix="", values={}):

    def make_category_field(data,values):
        name=data["name"]
        help_text=data["description"]       

    def make_string_field(data,values):
        name=data["name"]
        if name in values.keys():
            initial=values[name]
        else:
            initial=data["default"]
        help_text=data["description"]
        required=True        
        field={name:forms.CharField(initial=initial,help_text=help_text,max_length=100, label=name,required=required)}  
        return field

    def make_float_field(data,values):
        name=data["name"]
        if name in values.keys():
            initial=values[name]
        else:
            initial=data["default"]
        help_text=data["description"]
        required=True 
        field={name:forms.FloatField(initial=initial,help_text=help_text,label=name,required=required)}  
        return field


    make_field={
        "string":make_string_field,
        "float":make_float_field
    }

    fields={}


    data=ports["data"]

    for f in data:
        field_data=data[f]
        field_type=field_data["type"]

        if field_type != "category":
            field=make_field[field_type](field_data,values)
            fields.update(field)

    form=type('SimulationIOForm', (forms.BaseForm,), { 'base_fields': fields })

    # add prefix to form widgets
    form.prefix=prefix

    return form


    

