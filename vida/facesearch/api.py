from django.conf.urls import url
from tastypie.utils import trailing_slash
from tastypie import fields
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import Authorization
from tastypie.bundle import Bundle
from tastypie.resources import Resource
from vida.fileservice.helpers import get_fileservice_files, get_filename_absolute, get_fileservice_dir, get_gallery_file
from vida.vida.models import Person
from vida import br
from helpers import reindex_gallery
import subprocess

import hashlib
import os
import tempfile
import datetime

import logging
logger = logging.getLogger(__name__)


class FaceSearch(object):
    name = ''


class FaceSearchResource(Resource):
    name = fields.CharField(attribute='name')

    class Meta:
        resource_name = 'facesearchservice'
        object_class = FaceSearch
        fields = ['name']
        include_resource_uri = False
        allowed_methods = ['post']
        always_return_data = True
        authentication = BasicAuthentication()
        authorization = Authorization()

    def determine_format(self, request):
        return 'application/json'

    def deserialize(self, request, data, format=None):
        if not format:
            format = request.META.get('CONTENT_TYPE', 'application/json')

        if format == 'application/x-www-form-urlencoded':
            return request.POST

        if format.startswith('multipart'):
            data = request.POST.copy()
            data.update(request.FILES)
            return data

        return super(Resource, self).deserialize(request, data, format)

    def detail_uri_kwargs(self, bundle_or_obj):
        if isinstance(bundle_or_obj, Bundle):
            return {'name': bundle_or_obj.obj.name}
        else:
            return {'name': bundle_or_obj.name}

    def prepend_urls(self):
        """ Add the following array of urls to the Tileset base urls """
        return [
            url(r"^(?P<resource_name>%s)/test_getfilename%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('test_getfilename'), name="test_getfilename"),
            url(r"^(?P<resource_name>%s)/reload_gallery%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('reload_gallery'), name="reload_gallery"),
        ]

    # This function is a REST end-point to perform a simple test of br_get_filename, which is giving us a problem
    # Make sure to have a picture /tmp/testimage1.jpg
    def test_getfilename(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        res = []

        # create a new File
        filename_name = u'/tmp/testimage1.jpg'
        file_data = open(filename_name, 'rb').read()

        facetmpl = br.br_load_img(file_data, len(file_data))
        print "Setting file name on template to " + os.path.basename(filename_name)
        logger.debug("Setting file name on template to " + os.path.basename(filename_name))
        br.br_set_filename(facetmpl, os.path.basename(filename_name))
        print "Retrieving file name from template"
        logger.debug("Retriving file name from template")
        filename = br.br_get_filename(facetmpl)
        logger.debug("Filename=" + filename)
        print filename
        response = self.create_response(request, res)
        return response

    def reload_gallery(self, request, **kwargs):
        reindex_gallery()
        galleryGalPath = get_gallery_file()
        galGallery = br.br_make_gallery(galleryGalPath)
        galTemplateList = br.br_load_from_gallery(galGallery)

        # compare and collect scores
        ntargets = br.br_num_templates(galTemplateList)
        logger.debug(str(ntargets) + " templates found in the gallery at " + galleryGalPath)
        res = str(ntargets) + " templates found in the gallery at " + galleryGalPath
        for r in range(ntargets):
            tmpl = br.br_get_template(galTemplateList, r)
            logger.debug("Filename = " + br.br_get_filename(tmpl))
        response = self.create_response(request, res)
        br.br_free_template_list(galTemplateList)
        br.br_close_gallery(galGallery)
        return response

    def obj_create(self, bundle, request=None, **kwargs):
        # create a new File
        bundle.obj = FaceSearch()
        # full_hydrate does the heavy lifting mapping the
        # POST-ed payload key/values to object attribute/values
        bundle = self.full_hydrate(bundle)
        file_data = bundle.data[u'file'].read()

        # write the file data to a temporary file
        filename_name, file_extension = os.path.splitext(bundle.data[u'file'].name)
        destination_file = tempfile.NamedTemporaryFile(suffix=file_extension)
        destination_file.write(bytearray(file_data))
        destination_file.flush()
        os.fsync(destination_file) # Need this, we were not getting all bytes written to file before proceeding

        temp_gal = tempfile.NamedTemporaryFile(suffix='.gal')
        args = ['br', '-algorithm', 'FaceRecognition', '-enroll', destination_file.name, temp_gal.name]
        subprocess.call(args)
        out_file = tempfile.NamedTemporaryFile(suffix='.csv')
        galleryGalPath = get_gallery_file()
        args = args[:3] + ['-compare', galleryGalPath, temp_gal.name, out_file.name]
        subprocess.call(args)

        with open(out_file.name, 'r') as scores_file:
            files_line = scores_file.readline().strip().split(',')[1:]
            scores_line = scores_file.readline().strip().split(',')
            probe = scores_line[0]
            score_list = scores_line[1:]
            scores= []
            for f, s in zip(files_line, score_list):
                logger.debug('%s -> %s: %s' % (probe, f, s))
                scores.append((os.path.basename(f), s))

        destination_file.close()
        out_file.close()
        temp_gal.close()

        peeps = Person.objects.filter(pic_filename__in=dict(scores).keys()).values()

        sorted_peeps = []

        scores.sort(key=lambda s: s[1], reverse=True)
        # TODO: Make 15 a parameter - right now we return the top 15 results
        logger.debug("Building result package")
        for s in scores[:15]:
            currfilename = s[0]
            logger.debug(currfilename)
            foundPeep = filter(lambda p: p['pic_filename'] == os.path.basename(s[0]), peeps)
            if foundPeep is not None and len(foundPeep) > 0:
                sorted_peeps.append(foundPeep[0])
            else:
                logger.info("Found picture with no link person " + currfilename)

        # bundle the search results
        bundle.obj.name = bundle.data[u'file'].name
        bundle.data.pop(u'file', None)
        bundle.data['meta'] = {
            "limit": len(peeps),
            "next": None,
            "offset": 0,
            "previous": None,
            "total_count": len(peeps)
        }

        bundle.data['objects'] = sorted_peeps
        bundle.data['scores'] = scores
        return bundle

