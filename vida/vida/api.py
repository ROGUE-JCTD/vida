from tastypie.resources import ModelResource
from tastypie.authentication import BasicAuthentication
from .models import Person
from tastypie import fields
from django.contrib.auth import get_user_model


class UserResource(ModelResource):
    class Meta:
        queryset = get_user_model().objects.all()
        fields = ['username', 'first_name', 'last_name']
        resource_name = 'created_by'


class PersonResource(ModelResource):
    created_by = fields.ToOneField(UserResource, 'created_by',  full=True, blank=True, null=True)

    class Meta:
        queryset = Person.objects.all()
        excludes = ['start_date', 'stop_date']
        authentication = BasicAuthentication()

    def determine_format(self, request):
        return 'application/json'