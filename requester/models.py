from django.db import models



class RequesterData(models.Model):
    ID = models.AutoField(primary_key=True)
    From = models.CharField(max_length=100)
    To = models.CharField(max_length=100)
    dateandtime = models.CharField(max_length=50)
    assets = models.IntegerField()
    asset_type =  models.CharField(max_length=20)
    asset_sensitivity =  models.CharField(max_length=20)
    status = models.CharField(default="pending", max_length=20)
    applied = models.CharField(default="Not Applied", max_length=20)
    
    def __str__(self):
        return f"{self.From} -> {self.To}"