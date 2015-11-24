from django.contrib import admin
from vida.vida.models import Person, Shelter
import uuid

class PersonAdmin(admin.ModelAdmin):
    fields = ['created_by', 'shelter_id', 'family_name', 'given_name', 'gender', 'age', 'description', 'street_and_number', 'city', 'province_or_state', 'neighborhood', 'notes', 'barcode']
    list_display = ('family_name', 'given_name', 'gender', 'age', 'created_by')
    search_fields = ['family_name', 'given_name', 'notes', 'barcode', 'shelter_id']

admin.site.register(Person, PersonAdmin)

class ShelterAdmin(admin.ModelAdmin):
    fields = ['created_by', 'name', 'description', 'street_and_number', 'city', 'province_or_state', 'neighborhood', 'notes', 'geom']
    list_display = ('name', 'created_by', 'neighborhood')
    search_fields = ['name', 'street_and_number', 'city', 'province_or_state', 'neighborhood', 'uuid']

    def save_model(self, request, obj, form, change):
        obj.uuid = str(uuid.uuid4()).decode('unicode-escape') # Make new uuid for shelter
        return super(ShelterAdmin, self).save_model(request, obj, form, change)

admin.site.register(Shelter, ShelterAdmin)