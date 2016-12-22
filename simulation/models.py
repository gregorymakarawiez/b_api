from django.db import models


class Simulation(Publishable):
    component=models.ForeignKey('Component')
    inlet_data=models.TextField()
    outlet_data=models.TextField()

              

 


