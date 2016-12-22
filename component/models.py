import django
import jsonpickle
import simplejson as json
import six
from enum import Enum
from django.db import models
from django.utils import timezone
from B_Api.models import Publishable
from B_Api.widgets import ScriptWidget



"""class Port(models.Model):

    class IO_Type(Enum):
        UNDEFINED=0
        INLET=1
        OUTLET=2
 
    DATA_TYPE_CHOICES=(
    ('String','String'),
    ('Float','Float'),
    )

    DATA_CONSTRUCTORS={'String': {'constructor':models.TextField,'parameters':{'default':""}},
                       'Float':  {'constructor':models.FloatField,'parameters':{'default':0}},
                      }

    name = models.CharField(max_length=200)
    io_type =IO_Type.UNDEFINED 
    data_type= models.CharField(choices=DATA_TYPE_CHOICES, max_length=10, default='String') 
    
    # select and use constructor suited to data type
    data_constructor=DATA_CONSTRUCTORS[data_type.default]['constructor']
    parameters=DATA_CONSTRUCTORS[data_type.default]['parameters']
    value=data_constructor(**parameters)

    def __str__(self):
        return self.name
   
    class Meta:
        abstract=True

class I_Port(Port):

    io_type = Port.IO_Type.INLET
    #component = models.ForeignKey('Component',on_delete=models.CASCADE,related_name="i_ports")

class O_Port(Port):

    io_type = Port.IO_Type.OUTLET
    #component = models.ForeignKey('Component',on_delete=models.CASCADE,related_name="o_ports")


   class Script(models.Model):

    LANGUAGE_CHOICES=(
    ("python", "Python"),
    )


    name = models.CharField(max_length=200, default="")
    language = models.CharField(choices=LANGUAGE_CHOICES, max_length=20, default="python")
    script  = models.TextField(default="")

    def __str__(self):
        return self.name"""


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
    #outlet_ports=models.TextField()
    function = models.TextField() 
    jacobian = models.TextField() 

              

 


