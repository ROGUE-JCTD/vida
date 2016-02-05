from django.conf import settings
from django.contrib.gis.db import models
from django.db.models.signals import post_init
from django.contrib.gis.geos import Point
import helpers
import datetime

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

    site_details = models.CharField(blank=True, max_length=200)

    notes = models.TextField(blank=True)
    geom = models.PointField(srid=4326, default='POINT(0.0 0.0)')
    uuid = models.CharField(blank=False, max_length=100)

    def __unicode__(self):
        return self.name


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

    SHELTER_CHOICES = [] # will be created dynamically, this is to init shelter_id to have choices

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # time travel / versioning fields
    start_date = models.DateTimeField(null=True)
    stop_date = models.DateTimeField(null=True)

    # basic
    family_name = models.CharField(blank=True, max_length=50)
    given_name = models.CharField(blank=False, max_length=50)
    gender = models.CharField(blank=True, max_length=20)
    age = models.CharField(blank=True, max_length=10)
    mothers_given_name = models.CharField(blank=True, max_length=50)
    fathers_given_name = models.CharField(blank=True, max_length=50)
    date_of_birth = models.CharField(blank=True, max_length=50)

    description = models.TextField(blank=True)

    # address
    street_and_number = models.CharField(blank=True, max_length=100)
    neighborhood = models.CharField(blank=True, max_length=50)
    city = models.CharField(blank=True, max_length=50)
    province_or_state = models.CharField(blank=True, max_length=50)

    phone_number = models.CharField(blank=True, max_length=40)

    # this will store a uuid of the shelter on creation (can be used for database indexing)
    shelter_id = models.CharField(blank=True, max_length=100, choices=SHELTER_CHOICES, default='None')

    # this will be a uuid of each person so it can be later referenced for version-ing
    uuid = models.CharField(blank=False, max_length=100, default='None')

    notes = models.TextField(blank=True)

    barcode = models.CharField(null=True, blank=True, max_length=100)

    injury = models.CharField(blank=True, max_length=100)
    nationality = models.CharField(blank=True, max_length=100)
    status = models.CharField(blank=True, max_length=100)

    pic_filename = models.CharField(null=True, blank=True, max_length=50)

    geom = models.PointField(srid=4326, default='POINT(0.0 0.0)')

    # Set what fields we care about in the person record being changed from a history perspective.
    # we may not care about all fields being logged as changed
    @property
    def change_track_fields(self):
        return ('geom', 'given_name', 'family_name')

    def __init__(self, *args, **kwargs):
        super(Person, self).__init__(*args, **kwargs)
        SHELTER_CHOICES = []
        for i, shelter in enumerate(Shelter.objects.all()):
            SHELTER_CHOICES.append('')  # will create index for list, dynamically updating the size
            SHELTER_CHOICES[i] = (shelter.uuid, shelter.name)   # overwrite that index with choice (as tuple)
        self._meta.get_field_by_name('shelter_id')[0]._choices = SHELTER_CHOICES

    def __unicode__(self):
        return self.given_name

    def add_location_history(self):
        curr_value = getattr(self, 'geom')
        orig_value = getattr(self, '_original_geom')
        if curr_value != orig_value:
            # we have a hit! new geom is different.  Add it to the history, note that we
            # want to check for an older one and close it
            print("geometry changed")
            change = PersonLocationHistory.objects.create(geom=curr_value, start_date=datetime.datetime.now(),
                                                          person=self)
            self.personlocationhistory_set(change)

    def save(self, *args, **kwargs):
        # Customized the save method to update change history
        # if the private key is not null then the person exists, otherwise don't bother checking
        existing_person = bool(self.pk)
        # go ahead and save the changes
        super(Person, self).save(*args, **kwargs)  # Save the Person data to the DB
        if existing_person:
            # First, check if we have a new geometry, if so then store it in location history
            self.add_location_history()
            # TODO: if other fields have changed then log in the change history table


# Whenever a person model is initialized we make a copy of the current fields for the person object,
# that way we can check for changes and update the appropriate history table(s)
def person_post_init(sender, instance, **kwargs):
    if instance.pk:
        for field in instance.change_track_fields:
            setattr(instance, '_original_%s' % field, getattr(instance, field))

post_init.connect(person_post_init, sender=Person, dispatch_uid='vida.person.person_post_init')


class PersonLocationHistory(models.Model):
    geom = models.PointField(srid=4326, default='POINT(0.0 0.0)')
    start_date = models.DateTimeField(null=True)
    stop_date = models.DateTimeField(null=True)
    person = models.ForeignKey(Person, on_delete=models.PROTECT)
    shelter = models.ForeignKey(Shelter, on_delete=models.PROTECT, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
