from django import forms
from B_Api.widgets import MyQuillWidget
from component.models import Component



class SimulationForm(forms.Form):

    name= forms.CharField(max_length=200, label="Name", required=True) 
    description = forms.CharField(widget=MyQuillWidget)
    component = forms.ModelChoiceField(queryset=Component.objects.all(),empty_label=None)
 
    def clean_author(self):
        return request.user

    def clean_created_date(self):
        return timezone.now()

    def clean_modified_date(self):
        return timezone.now()

    def clean_published_date(self):
        return timezone.now()




