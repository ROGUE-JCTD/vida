from django.db import models
from django.conf import settings
import helpers


class Person(models.Model):

    HEALTH_TREATMENT_CHOICES = [
        (0, 'Unknown'),
        (1, 'None'),
        (2, 'In Progress'),
        (3, 'Completed')]

    STATUS_CHOICES = [
        (0, 'Unknown'),
        (1, 'Displaced'),
        (2, 'Lost'),
        (3, 'Found')]

    GENDER_CHOICES = [
        (0, 'Unknown'),
        (1, 'Male'),
        (2, 'Female'),
        (3, 'Other')]

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # time travel / versioning fields
    start_date = models.DateTimeField(null=True)
    stop_date = models.DateTimeField(null=True)

    # basic
    family_name = models.CharField(blank=True, max_length=50)
    given_name = models.CharField(blank=False, max_length=50)
    gender = models.CharField(blank=True, max_length=10)
    age = models.CharField(blank=True, max_length=10)
    mothers_given_name = models.CharField(blank=True, max_length=50)
    fathers_given_name = models.CharField(blank=True, max_length=50)

    description = models.TextField(blank=True)

    # address
    street_and_number = models.CharField(blank=True, max_length=100)
    neighborhood = models.CharField(blank=True, max_length=50)
    city = models.CharField(blank=True, max_length=50)
    province_or_state = models.CharField(blank=True, max_length=50)

    # if shelters are versioned time-travel extension like, then we have to store a key as opposed to id of row
    shelter = models.CharField(blank=True, max_length=50)

    notes = models.TextField(blank=True)

    barcode = models.IntegerField(null=True, blank=True)
    pic_filename = models.CharField(null=True, blank=True, max_length=50)

    def __unicode__(self):
        return self.given_name


class Shelter(models.Model):

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    # time travel / verioning fields
    #start_date = models.DateTimeField(blank=True)
    #stop_date = models.DateTimeField(blank=True)

    # basic
    name = models.CharField(blank=True, max_length=50)
    description = models.TextField(blank=True)

    # address
    street_and_number = models.CharField(blank=True, max_length=100)
    neighborhood = models.CharField(blank=True, max_length=50)
    city = models.CharField(blank=True, max_length=50)
    province_or_state = models.CharField(blank=True, max_length=50)

    notes = models.TextField(blank=True)

    def __unicode__(self):
        return self.name
