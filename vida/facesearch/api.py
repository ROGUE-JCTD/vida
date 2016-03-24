from tastypie import fields
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import Authorization
from tastypie.bundle import Bundle
from tastypie.resources import Resource
from vida.fileservice.helpers import get_fileservice_files, get_filename_absolute
from vida.vida.models import Person
from brpy import init_brpy
import os
import sys

import hashlib
import tempfile

import logging
logger = logging.getLogger(__name__)

class FaceSearch(object):
    name = ''


class FaceSearchResource(Resource):
    name = fields.CharField(attribute='name')
    br = init_brpy()
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

    def obj_create(self, bundle, request=None, **kwargs):
        # create a new File
        print "running face search"
        bundle.obj = FaceSearch()
        # full_hydrate does the heavy lifting mapping the
        # POST-ed payload key/values to object attribute/values
        bundle = self.full_hydrate(bundle)
        file_data = bundle.data[u'file'].read()
        # write the file data to a temporary file TODO: can we load directly from the file stream?  Ask Jordan
        filename_name, file_extension = os.path.splitext(bundle.data[u'file'].name)
        destination_file = tempfile.NamedTemporaryFile(suffix=file_extension)
        destination_file.write(bytearray(file_data))
        destination_file.flush()
        os.fsync(destination_file) # Need this, we were not getting all bytes written to file before proceeding
        logger.debug("Wrote temporary file " + destination_file.name)
        try:
            self.br.br_initialize_default()
            self.br.br_set_property('algorithm', 'FaceRecognition')
            self.br.br_set_property('enrollAll', 'true')
            facetmpl = self.br.br_load_img(file_data, len(file_data))
            query = self.br.br_enroll_template(facetmpl)
            nqueries = self.br.br_num_templates(query)
            scores = []
            file_names = get_fileservice_files()
            for currFile in file_names:
                if 'thumb' in currFile:
                    continue
                print ("Comparing " + currFile)
                _name, _extension = os.path.splitext(currFile)
                img = open(get_filename_absolute(currFile), 'rb').read()
                tmpl = self.br.br_load_img(img, len(img))
                targets = self.br.br_enroll_template(tmpl)
                ntargets = self.br.br_num_templates(targets)
                # compare and collect scores
                scoresmat = self.br.br_compare_template_lists(targets, query)
                for r in range(ntargets):
                    for c in range(nqueries):
                        # This is not a percentage match, it's a relative score
                        similarity = self.br.br_get_matrix_output_at(scoresmat, r, c)
                        scores.append(('{}{}'.format(hashlib.sha1(img).hexdigest(), _extension), similarity))

                # clean up - no memory leaks
                self.br.br_free_template(tmpl)
                self.br.br_free_template_list(targets)
        except:
            logger.error("Unexpected error ")
            logger.error(sys.exc_info()[0])
            print ("Unexpected error ")
            print(sys.exc_info()[0])
            raise

        destination_file.close()
        self.br.br_free_template(facetmpl)
        self.br.br_finalize()

        peeps = Person.objects.filter(pic_filename__in=dict(scores).keys()).values()

        sorted_peeps = []

        scores.sort(key=lambda s: s[1], reverse=True)
        # TODO: Make 15 a parameter - right now we return the top 15 results
        for s in scores[:15]:
            print s[0]
            sorted_peeps.append(filter(lambda p: p['pic_filename'] == s[0], peeps)[0])

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
