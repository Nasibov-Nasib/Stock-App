
import time
import datetime as d
from math import ceil
from unicodedata import name
from django.db import models
from django.core.validators import MinLengthValidator,MaxLengthValidator
from django.contrib.auth.models import User

# Create your models here.



    
class Brands(models.Model):
   
    Brand = models.CharField('Brand',max_length= 50)
    Foto = models.FileField(upload_to='images/' ,  blank=True)
    Tarix = models.DateField(auto_now=True)
    user_id = models.CharField(max_length=50)

    def __str__(self):
        return self.Brand

    def get_absolute_url(self):
        return f'/'
        
class Clients(models.Model):
    
    Ad = models.CharField('Ad',max_length=50)
    Soyad = models.CharField(max_length=50)
    Tel = models.CharField(max_length=50)
    Foto = models.FileField(upload_to='images/')
    Email = models.EmailField(max_length=50)
    Sirket = models.CharField(max_length=50)
    Tarix = models.DateField(auto_now=True)
    user_id = models.IntegerField()
    def __str__(self):
        return self.Ad

    def get_absolute_url(self):
        return f'/'
class Xercler(models.Model):
    
    Teyinat = models.CharField(max_length=50)
    Mebleg = models.CharField(max_length=50)
    Tarix = models.DateField(auto_now=True)
    user_id = models.CharField(max_length=50)
    def __str__(self):
        return self.Teyinat

    def get_absolute_url(self):
        return f'/'

class Mehsul(models.Model):
    Brand_id = models.ForeignKey(Brands,on_delete=models.CASCADE)
    Ad = models.CharField(max_length=50)
    Foto = models.FileField(upload_to='images/')
    Alish = models.IntegerField(validators=[MaxLengthValidator(1000),MinLengthValidator(0)])
    Satish = models.IntegerField(validators=[MaxLengthValidator(1000),MinLengthValidator(0)])
    Miqdar = models.IntegerField(validators=[MaxLengthValidator(1000),MinLengthValidator(0)])
    user_id = models.CharField(max_length=50)

    @property
    def cem(self):
        qazanc = (self.Satish * self.Miqdar) - (self.Alish * self.Miqdar)
        return qazanc
    

    def __str__(self):
        return str(self.Brand_id)

    def get_absolute_url(self):
        return f'/'
    
    def brand_id(self):
        return self.part_set.select_related('Brand_id')
    
class Sifaris(models.Model):
    Client_id = models.ForeignKey(Clients,on_delete=models.CASCADE)
    Mehsul_id = models.ForeignKey(Mehsul,on_delete=models.CASCADE)
    Miqdar =  models.CharField(max_length=50)
    Tesdiq = models.IntegerField(validators=[MaxLengthValidator(1000),MinLengthValidator(0)])
    Tarix = models.DateField(auto_now=True)
    user_id = models.CharField(max_length=50)

    @property
    def cemsif(self):
        qazanc = (int(self.Mehsul_id.Satish) * int(self.Miqdar)) - (int(self.Mehsul_id.Alish) * int(self.Miqdar))
        return qazanc
    

    def __str__(self):
        return self.Client_id

    def get_absolute_url(self):
        return f'/'
    
class Shobe(models.Model):
    
    
    ad = models.CharField(max_length=50,blank=True)
    user_id = models.IntegerField()
    
    def __str__(self):
        return self.ad
    def get_absolute_url(self):
        return f'/'
    
class Vezife(models.Model):
    
    shobe_id = models.ForeignKey(Shobe , on_delete = models.CASCADE)
    user_id = models.IntegerField()
    ad = models.CharField(max_length=50)
    
    def __str__(self):
        return self.ad

    def get_absolute_url(self):
        return f'/'
    

class Ishciler(models.Model):
    
    ad =  models.CharField(max_length=50)
    soyad =  models.CharField(max_length=50)
    telefon =  models.CharField(max_length=50)
    ev_tel  =  models.CharField(max_length=50)
    unvan =  models.CharField(max_length=50)
    email =  models.EmailField(max_length=50)
    user_id = models.CharField(max_length=50)
    vezife_id = models.ForeignKey(Vezife , on_delete = models.CASCADE)

    
    def __str__(self):
        return str(self.ad)

    def get_absolute_url(self):
        return f'/'
    
class Senedler(models.Model):
    
    ishci_id =  models.ForeignKey(Ishciler,on_delete=models.CASCADE,blank=True,null=True)
    basliq = models.CharField(max_length = 50)
    skan =  models.FileField(upload_to='images/')
    qeyd =  models.CharField(max_length = 50)    
    user_id = models.IntegerField()


    def __str__(self):
        return self.ishci_id

    def get_absolute_url(self):
        return f'/'
    

    

class Profil(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    foto = models.FileField(upload_to='images/')
    us = models.CharField(max_length=10)

    def __str__(self):
        return self.us

    def get_absolute_url(self):
        return f'/'
    
class Tapsiriq(models.Model):
    tapsiriq = models.CharField(max_length=15)
    tarix = models.DateField(max_length=15)
    saat = models.TimeField(max_length=15)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    
    @property

    def qalanvaxt(self):
        tarix1 = d.datetime(self.tarix.year,self.tarix.month,self.tarix.day,self.saat.hour,self.saat.minute,0)
        tarix2 = d.datetime.now()
        t1 = time.mktime(tarix1.timetuple())
        t2 =  time.mktime(tarix2.timetuple())
        san =  ceil(t1-t2)
        deq = ceil(san/60)
        saat = ceil(deq/60)-1
        gun = ceil(saat/24)-1
        if gun<=0 and saat>0:
            q = saat
            return str(q) + ' saat' 
        elif gun<=0 and saat<=0 and deq>0:
            q = deq
            return str(q) + ' deq'
        elif gun>0:
            q = gun 
            return str(q) + ' gun'
        else:
            q = 0
            return q                   
            
    @property

    def tarix1(self):
        q = str(self.tarix)
        return q      

    
    
    
