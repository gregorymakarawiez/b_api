from django import forms
from django.utils.safestring import mark_safe
from django.template import loader, Template
from django.shortcuts import render
from django.template.loader import render_to_string

class PortEditorWidget(forms.Widget):

    def render(self, name, value, attrs=None): 


        template_name='component/port_editor/port_editor.html'
        context={'name':name,'value':value}
        html=render_to_string(template_name,context)


        return mark_safe(html)

 





