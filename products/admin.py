from django.contrib import admin

from .models import Product, Medicine, GeneralGood, MedicineForm, DosageUnit

admin.site.register(Product)
admin.site.register(Medicine)
admin.site.register(GeneralGood)
admin.site.register(MedicineForm)
admin.site.register(DosageUnit)