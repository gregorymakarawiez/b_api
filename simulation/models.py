from django.db import models
from B_Api.models import Publishable

class Simulation(Publishable):
    component=models.ForeignKey('component.Component')
    inlet_data=models.TextField()
    outlet_data=models.TextField()

              

 


