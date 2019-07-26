from django.db import models
class MyUser(models.Model):
    userName = models.CharField(max_length=10)
    password= models.CharField(max_length=10)
    cpassword= models.CharField(max_length=10)
    fname= models.CharField(max_length=10)
    lname= models.CharField(max_length=10)
    email=models.EmailField(max_length=30)
    mobno=models.IntegerField()
    dob=models.DateField()

