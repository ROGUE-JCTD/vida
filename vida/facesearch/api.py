from tastypie import fields
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import Authorization
from tastypie.bundle import Bundle
from tastypie.resources import Resource

from vida import br
from vida.fileservice.helpers import get_gallery_file
from vida.vida.models import Person

import os


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

    def obj_create(self, bundle, request=None, **kwargs):
        # create a new File
        bundle.obj = FaceSearch()
        # full_hydrate does the heavy lifting mapping the
        # POST-ed payload key/values to object attribute/values
        bundle = self.full_hydrate(bundle)
        file_data = bundle.data[u'file'].read()
        filename_name, file_extension = os.path.splitext(bundle.data[u'file'].name)

        # Load uploaded image with OpenBR
        facetmpl = br.br_load_img(file_data, len(file_data))
        query = br.br_enroll_template(facetmpl)

        # Open the OpenBR gallery file
        galleryGalPath = get_gallery_file()
        galGallery = br.br_make_gallery(galleryGalPath)
        galTemplateList = br.br_load_from_gallery(galGallery)

        # compare and collect scores
        nqueries = br.br_num_templates(query)
        ntargets = br.br_num_templates(galTemplateList)
        scoresmat = br.br_compare_template_lists(galTemplateList, query)
        scores = []
        for r in range(ntargets):
            for c in range(nqueries):
                # This is not a percentage match, it's a relative score
                similarity = br.br_get_matrix_output_at(scoresmat, r, c)
                tmpl = br.br_get_template(galTemplateList, r)
                # TODO: This doesn't seem to work through PyCharm, but does once deployed
                # Plus, it's not correlating filenames to templates correctly.
                #filename = br.br_get_filename(tmpl)
                #scores.append((os.path.basename(filename), similarity))
                scores.append(('replace-me', similarity))

        # clean up - no memory leaks
        br.br_free_template(facetmpl)
        br.br_free_template_list(query)
        br.br_free_template_list(galTemplateList)
        br.br_close_gallery(galGallery)

        scores.sort(key=lambda s: s[1], reverse=True)
        peeps = Person.objects.filter(pic_filename__in=dict(scores).keys()).values()

        # TODO: Make 15 a parameter - right now we return the top 15 results
        sorted_peeps = []
        for s in scores[:15]:
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
