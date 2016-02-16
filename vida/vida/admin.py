# from django.contrib import admin
from django.contrib.gis import admin
from django.contrib.gis.geos import (Point, GEOSGeometry)
from vida.vida.models import Person, Shelter
import uuid
import helpers


class PersonAdmin(admin.GeoModelAdmin):
    fields = ['created_by', 'shelter_id', 'family_name', 'given_name', 'gender', 'age', 'description', 'street_and_number', 'city', 'province_or_state', 'neighborhood', 'notes', 'barcode', 'geom']
    list_display = ('given_name', 'family_name', 'gender', 'age', 'created_by')
    search_fields = ['given_name', 'family_name', 'notes', 'barcode']
    default_lon = -61.45
    default_lat = 10.65
    default_zoom = 12

    def save_model(self, request, obj, form, change):
        obj.uuid = str(uuid.uuid4()).decode('unicode-escape') # Make new uuid for person (important for version-ing)
        return super(PersonAdmin, self).save_model(request, obj, form, change)

admin.site.register(Person, PersonAdmin)


class ShelterAdmin(admin.GeoModelAdmin):
    actions = ['delete_selected']
    fields = ['created_by', 'name', 'description', 'street_and_number', 'city', 'province_or_state', 'neighborhood', 'notes', 'geom']
    list_display = ('name', 'created_by', 'neighborhood')
    search_fields = ['name', 'street_and_number', 'city', 'province_or_state', 'neighborhood', 'uuid']

    default_lon = -61.45
    default_lat = 10.65
    default_zoom = 12

    def save_model(self, request, obj, form, change):
        obj.uuid = str(uuid.uuid4()).decode('unicode-escape') # Make new uuid for shelter
        obj.site_details = str('http://' + helpers.get_network_ip('eth1') + '/shelters/')
        return super(ShelterAdmin, self).save_model(request, obj, form, change)

    def response_post_save_add(self, request, obj):
        obj.site_details += str(obj.id) + '/'
        obj.save() # This adds the ID after the save, because Django doesn't have the ID field before creation
        return super(ShelterAdmin, self).response_post_save_add(request, obj)

    def delete_selected(self, request, obj):
        for shelter in obj.all(): # All selected shelters
            for i, person in enumerate(Person.objects.all()): # Find whoever (people) had that shelter uuid (optimize?)
                if person.shelter_id == shelter.uuid:
                     person.shelter_id = ''.decode('unicode-escape')  # Shelter has been removed, no need for them to hold shelterID anymore
                     person.save()
            shelter.delete()

admin.site.register(Shelter, ShelterAdmin)