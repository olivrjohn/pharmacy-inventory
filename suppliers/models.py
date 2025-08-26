from django.db import models

class Suppliers(models.Model):
    """General information about suppliers"""
    name = models.CharField(max_length=150)
    address = models.TextField()
    telephone_number = models.CharField(max_length=25)
    mobile_number = models.CharField(max_length=15)
    email_address = models.EmailField()
    contact_person = models.CharField(max_length=150)
    remarks = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
