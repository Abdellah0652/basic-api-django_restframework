from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import *
# Register your models here.


class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'dtype', 'doc_number')

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'active')

class ProfessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'description')

class DataSheetAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'historical_data')

admin.site.register(Document, DocumentAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Profession, ProfessionAdmin)
admin.site.register(DataSheet, DataSheetAdmin)