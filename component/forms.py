from django import forms
from .models import Component #, I_Port, O_Port
from B_Api.widgets import MyAceWidget, MyQuillWidget
from component.widgets import PortEditorWidget


'''class PortEditorField(forms.MultiValueField):
    widget = PortEditorWidget

    def __init__(self, *args, **kwargs):
        super(PortEditorField, self).__init__(*args, **kwargs)
        fields = (
            forms.CharField(),
            forms.CharField()
        )

    def compress(self, data_list):
        return ' '.join(data_list)'''


class ComponentForm(forms.Form):

    name= forms.CharField(max_length=200) 
    description= forms.CharField(widget=MyQuillWidget)
    inlet_ports= forms.CharField(widget=PortEditorWidget)
    #outlet_ports= forms.CharField(widget=PortEditorWidget) 
    function=forms.CharField(widget=MyAceWidget) 
    jacobian=forms.CharField(widget=MyAceWidget)

"""class ComponentForm_Old(forms.ModelForm):    

    class Meta:
        model = Component
        fields = ('name', 'description','function','jacobian')"""
