from django.contrib import admin

from vida.vida.models import Person, Shelter


class PersonAdmin(admin.ModelAdmin):
    fields = ['created_by', 'family_name', 'given_name', 'gender', 'age', 'description', 'street_and_number', 'city', 'province_or_state', 'neighborhood', 'notes', 'barcode']
    list_display = ('family_name', 'given_name', 'gender', 'age', 'created_by')
    search_fields = ['family_name', 'given_name', 'notes', 'barcode']

admin.site.register(Person, PersonAdmin)

class ShelterAdmin(admin.ModelAdmin):
    fields = ['created_by', 'name', 'description', 'street_and_number', 'city', 'province_or_state', 'neighborhood', 'notes', 'geom']
    list_display = ('name', 'created_by', 'neighborhood')
    search_fields = ['name', 'street_and_number', 'city', 'province_or_state', 'neighborhood']

admin.site.register(Shelter, ShelterAdmin)