from django import forms
from .models import Component #, I_Port, O_Port
from B_Api.widgets import MyAceWidget, MyQuillWidget
from component.widgets import PortEditorWidget




class ComponentForm(forms.Form):

    name= forms.CharField(max_length=200) 
    description= forms.CharField(widget=MyQuillWidget)
    inlet_ports= forms.CharField(widget=PortEditorWidget)
    outlet_ports= forms.CharField(widget=PortEditorWidget) 
    function=forms.CharField(widget=MyAceWidget) 
    jacobian=forms.CharField(widget=MyAceWidget)


