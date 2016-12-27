import django
import jsonpickle
import simplejson as json
import six
from enum import Enum
from django.db import models
from django.utils import timezone
from B_Api.models import Publishable
from B_Api.widgets import ScriptWidget




class PythonField(models.TextField):

    def __init__(self, *args,**kwargs):
        self.model_class=self.__class__.__name__.strip('Field')
        super(PythonField,self).__init__(*args,**kwargs)
  

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        try:
            # text->json
            json_obj=json.loads(value)
            # json->object
            obj=jsonpickle.decode(json_obj)
        except:
            obj=None

        return obj


    def to_python(self, value):
        if value.__class__.__name__== self.model_class:
            return value

        if value is None:
            return value

        try:
            # txt->json
            json_obj= json.loads(value) 
            # json->object
            obj=jsonpickle.decode(json_obj)
        except:
            obj=None

        return obj

    def get_prep_value(self, value):
        if not value:
            return ""
        else:
            try:
                # object->json
                json_obj=jsonpickle.encode(value)
                # json->txt
                txt=json.dumps(json_obj)
            except:
                txt=""  
            return txt

    def db_type(self, connection):
        return self.__class__.__name__.strip('from B_Api.widgets import MyAceWidgetField').lower()



class JsonField(models.TextField):

    def __init__(self, *args,**kwargs):
        #self.model_class=self.__class__.__name__.strip('Field')
        super(JsonField,self).__init__(*args,**kwargs)
  

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        try:
            # text->json
            obj=json.loads(value)

        except:
            obj=None

        return obj


    def to_python(self, value):
        if is_json(value):
            return value

        if value is None:
            return value

        try:
            # txt->json
            obj= json.loads(value) 

        except:
            obj=None

        return obj

    def get_prep_value(self, value):
        if not value:
            return ""
        else:
            try:
                # json->txt
                txt=json.dumps(value)
            except:
                txt=""  
            return txt

    def db_type(self, connection):
        return self.__class__.__name__.strip('from B_Api.widgets import MyAceWidgetField').lower()


    def is_json(value):
        try:
            txt = json.loads(value)
        except ValueError:
            return False
        
        return True


class Script(object):

    def __init__(self,language="python", txt=""):
        self.language=language
        self.txt=txt



class ScriptField(PythonField):

    widget=ScriptWidget
    #widget=django.forms.TextInput
    pass


class ScriptField2(models.TextField):
    
    #widget=ScriptWidget2
    widget=django.forms.HiddenInput



class Port(object):

    def __init__(self,name="", description="", default=None):
        self.name=name
        self.description=description
        self.type=self.__class__.__name__.strip('Port')
        self.default=default

    class Meta:
        abstract=True


class StringPort(Port):

    def __init__(self,default="",*args,**kwargs):

        try:
            isinstance(default,str)
        except TypeError as err:
            print("StringPort error: %s" % format(err))

        super(StringPort,self).__init__(default=default,*args,**kwargs)


class FloatPort(Port):

    def __init__(self,default=0,*args,**kwargs):

        try:
            isinstance(default,float)
        except TypeError as err:
            print("FloatPort error: %s" % format(err))

        super(FloatPort,self).__init__(default=default,*args,**kwargs)


class PortField(PythonField):

    #widget=django.forms.TextInput
    pass


class ListField(PythonField):

    #widget=django.forms.TextInput
    pass


class Component(Publishable):
    inlet_ports=models.TextField()
    outlet_ports=models.TextField()
    function = models.TextField() 
    jacobian = models.TextField() 

              

 


