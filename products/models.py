from django.db import models

class ProductCategory(models.TextChoices):
    """Constant choices for product category."""
    GENERAL_GOODS = "GG", "General Goods"
    MEDICINE = "MEDICINE", "Medicine"

class MedicineType(models.TextChoices):
    """Constant choices for medicine type."""
    OTC = "OTC", "Over-the-counter"
    PRESCRIPTION = "PRESCRIPTION", "Prescription Drugs"

class Product(models.Model):
    """General details about the product of the inventory."""
    brand = models.CharField(max_length=150)
    name = models.CharField(max_length=150)
    category = models.CharField(max_length=10, choices=ProductCategory.choices, default=ProductCategory.MEDICINE)
    # Will monitor and check if description should still be included in the product model or if it should be model specific
    # description = models.TextField()
    status = models.CharField(max_length=15, default="DRAFT") # will be used to create draft products before publishing
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        """Return a string representation of the model."""
        return self.name

class MedicineForm(models.Model):
    """Data of forms of medicines."""
    name = models.CharField(max_length=30)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of the model."""
        return self.name

class DosageUnit(models.Model):
    """Data for units of medicines."""
    name = models.CharField(max_length=10)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of the model."""
        return self.name
    
class Medicine(models.Model):
    """Details of a product specific to medicines."""
    product = models.OneToOneField(Product, limit_choices_to={'category': ProductCategory.MEDICINE}, on_delete=models.CASCADE)
    generic_name = models.CharField(max_length=250)
    dosage = models.CharField(max_length=150)
    form = models.ForeignKey(MedicineForm, on_delete=models.CASCADE)
    usage = models.TextField()
    side_effects = models.TextField()
    prescription_type = models.CharField(max_length=15, choices=MedicineType.choices, default=MedicineType.PRESCRIPTION)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of the model."""
        return self.generic_name
    
class GeneralGood(models.Model):
    """Details of a product specific to general goods."""
    product = models.OneToOneField(Product, limit_choices_to={'category': ProductCategory.GENERAL_GOODS}, on_delete=models.CASCADE)
    # name = models.CharField(max_length=100) will remove for now and base only on product name
    type = models.CharField(max_length=35)
    unit = models.CharField(max_length=20, default="-")
    notes = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of the model."""
        return self.product.name