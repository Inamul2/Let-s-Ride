from django.db import models



class RiderData(models.Model):
    ID = models.AutoField(primary_key=True)
    From = models.CharField(max_length=100)
    To = models.CharField(max_length=100)
    dateandtime = models.CharField(max_length=50)
    medium = models.CharField(max_length = 5)
    assets = models.IntegerField()
    
    def __str__(self):
        return f"{self.From} -> {self.To}"