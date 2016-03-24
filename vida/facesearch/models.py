from django.contrib.gis.db import models


class ImageTemplate(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)

    # for example, 38339293847298372.jpg
    filename = models.CharField(blank=False, null=False, max_length=250)
    image_template = models.BinaryField(blank=False, null=False)

    def __unicode__(self):
        return self.filename
