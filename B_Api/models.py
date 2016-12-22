from django.db import models
from django.utils import timezone


class Publishable(models.Model):
    name = models.CharField(max_length=200)
    author = models.ForeignKey('auth.User')
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(blank=True, null=True)

   
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.name

    class Meta:
        abstract=True 



