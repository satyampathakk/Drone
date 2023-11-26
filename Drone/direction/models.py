from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class LocationUpdate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Location Update for {self.user.username} at {self.timestamp}"


class UserDestination(models.Model):
    desired_lat=models.FloatField()
    desired_long=models.FloatField()
    timeStamp=models.DateTimeField(auto_now=True)
    name=models.CharField(max_length=200)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    

