from django.conf import settings
from django.contrib.gis.db import models
from django.db.models.signals import post_init
from django.contrib.gis.geos import (Point, GEOSGeometry)
import helpers
import logging
import datetime

logger = logging.getLogger(__name__)

class Shelter(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    # time travel / verioning fields
    # start_date = models.DateTimeField(blank=True)
    # stop_date = models.DateTimeField(blank=True)

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

    SHELTER_CHOICES = []  # will be created dynamically, this is to init shelter_id to have choices

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

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
        return 'given_name', 'family_name', 'gender', 'age', 'mothers_given_name', 'fathers_given_name','date_of_birth', 'street_and_number', 'neighborhood', 'city', 'province_or_state', 'phone_number', 'shelter_id', 'barcode', 'injury', 'nationality', 'status', 'pic_filename'

    def __init__(self, *args, **kwargs):
        super(Person, self).__init__(*args, **kwargs)
        SHELTER_CHOICES = []
        for i, shelter in enumerate(Shelter.objects.all()):
            SHELTER_CHOICES.append('')  # will create index for list, dynamically updating the size
            SHELTER_CHOICES[i] = (shelter.uuid, shelter.name)  # overwrite that index with choice (as tuple)
        self._meta.get_field_by_name('shelter_id')[0]._choices = SHELTER_CHOICES

    def __unicode__(self):
        return self.given_name

    def add_location_history(self):
        if hasattr(self, 'geom'):  # if there is no geometry then no need to record a history
            curr_value = getattr(self, 'geom')
            # now, check if there were any previous history entry for this person w/ no close date and close those
            is_new_geom = False
            if hasattr(self, '_original_geom'):
                orig_value = getattr(self, '_original_geom')
                if curr_value != orig_value:
                    print("Existing person, new location")
                    is_new_geom = True
            else:
                print("New person record, record their initial location")
                is_new_geom = True

            if is_new_geom:
                # we have a hit! new geom is different.  Add it to the history, note that we
                # want to check for an older one and close it
                print("geometry changed")
                for r in PersonLocationHistory.objects.filter(person_id=self.id, stop_date__isnull=True):
                    r.stop_date = datetime.datetime.now()
                    r.save()
                    print(r)
                new_record = PersonLocationHistory(geom=curr_value, start_date=datetime.datetime.now(),
                                                   person_id=self, created_by=self.created_by,
                                                   shelter_uuid=self.shelter_id)
                new_record.save()

    def add_field_history(self):
        # TODO: note: does not currently track 'notes' and 'description' fields. THose are TextField type, rather than
        # char type, so could be larger.  Need a use case discussion to determine how to handle
        # Also, this code only works for string field types.  If we add integer or date format fields
        # (like for age, DOB) then do we need to deal with type conversion?
        for field in self.change_track_fields:
            new_val = getattr(self, field)
            orig_val = getattr(self, '_original_%s' % field)
            if new_val != orig_val:
                new_record = PersonFieldHistory(field_name=field, date_of_change=datetime.datetime.now(),
                                                person=self, changed_by=self.created_by,
                                                old_value=orig_val, new_value=new_val)
                new_record.save()

    def save(self, *args, **kwargs):
        logger.debug("vida person.save with args")
        logger.debug(self.created_by)
        logger.debug(self.created_by_id)
        # check the args.  While the admin interface sends the user ID for the creator, the mobile app is giving us
        # the username.  So we have to detect which it is.  Note that we cannot accept NULL/no value for create_by

        # Customized the save method to update change history
        # if the private key is not null then the person exists, otherwise don't bother checking
        existing_person = bool(self.pk)
        # Put the current date/time in the updated_at field so we know when it was done
        self.updated_at = datetime.datetime.now();
        # go ahead and save the changes
        super(Person, self).save(*args, **kwargs)  # Save the Person data to the DB
        # First, check if we have a new geometry, if so then store it in location history, which we do
        # if the record is new or updated
        self.add_location_history()
        # TODO: if other fields have changed then log in the change history table
        if existing_person:
            self.add_field_history()


# Whenever a person model is initialized we make a copy of the current fields for the person object,
# that way we can check for changes and update the appropriate history table(s)
def person_post_init(sender, instance, **kwargs):
    if instance.pk:
        for field in instance.change_track_fields:
            setattr(instance, '_original_%s' % field, getattr(instance, field))

post_init.connect(person_post_init, sender=Person, dispatch_uid='vida.person.person_post_init')


class PersonLocationHistory(models.Model):
    geom = models.PointField(srid=4326, default='POINT(0.0 0.0)')
    start_date = models.DateTimeField(null=False)
    stop_date = models.DateTimeField(null=True)
    person_id = models.ForeignKey(Person, null=False, on_delete=models.PROTECT)
    shelter_uuid = models.CharField(blank=True, max_length=100, default='None')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)


class PersonFieldHistory(models.Model):
    field_name = models.CharField(blank=False, max_length=64, default='None')
    old_value = models.CharField(max_length=128)
    new_value = models.CharField(max_length=128)
    date_of_change = models.DateTimeField(null=False)
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    person = models.ForeignKey(Person, null=False, on_delete=models.PROTECT)
