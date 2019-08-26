from django.db import models

# Create your models here.
class DFI_Info(models.Model):
    Source_Mac = models.CharField(max_length=17)
    Dest_Mac = models.CharField(max_length=17)
    Source_IP = models.CharField(max_length=15)
    Dest_IP = models.CharField(max_length=15)
    Source_Port = models.CharField(max_length=5)
    Dest_Port = models.CharField(max_length=5)
    Protocol = models.CharField(max_length=20)
    Bytes = models.IntegerField()
    Host = models.CharField(max_length=300)
    Date = models.DateField(auto_now=True)
    Time = models.TimeField(auto_now=True)

    class Meta:
        db_table = 'DFI_Info'
        verbose_name = 'DFI Info'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.Source_IP


class DPI_Picture(models.Model):
    Source_IP = models.CharField(max_length=15)
    Dest_IP = models.CharField(max_length=15)
    Pic_Path = models.CharField(max_length=50)
    DateTime = models.DateTimeField()

    class Meta:
        db_table = 'DPI_Picture'
        verbose_name = 'DPI Picture'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.Dest_IP

'''
from django.db import models

# Create your models here.
class black_mac(models.Model):
    mac = models.CharField(max_length=20)
class attack(models.Model):
    attack_type = models.CharField(max_length=50)
    attacked_mac = models.CharField(max_length=20,null=True)
    attacker_mac = models.CharField(max_length=20,null=True)
    affected_mac = models.CharField(max_length=2000,null=True)
    attack_date = models.DateTimeField(auto_now=False)
'''
