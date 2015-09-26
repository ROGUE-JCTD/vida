from tastypie.authentication import BasicAuthentication
from tastypie.authorization import Authorization
from tastypie.utils import trailing_slash
from tastypie.bundle import Bundle
from django.core.urlresolvers import NoReverseMatch
from tastypie.exceptions import NotFound
from tastypie.resources import Resource
from django.conf.urls import url
from django.views.static import serve
from tastypie import fields
import helpers
import os


class FileItem(object):
    id = None
    name = ''


class FileItemResource(Resource):
    id = fields.IntegerField(attribute='id')
    name = fields.CharField(attribute='name')
    file = fields.FileField(attribute='file', null=True, blank=True)

    class Meta:
        resource_name = 'fileitem'
        object_class = FileItem
        fields = ['name']
        authentication = BasicAuthentication()
        authorization = Authorization()

    def determine_format(self, request):
        return 'application/json'

    @staticmethod
    def get_file_items():
        file_names = helpers.get_file_service_files()
        file_items = []
        fake_id = 0
        for name in file_names:
            file_item = FileItem()
            file_item.id = fake_id
            fake_id += 1
            file_item.name = name
            file_item.file = helpers.get_filename_absolute(name)
            file_items.append(file_item)
        return file_items


    @staticmethod
    def get_file_item(kwargs):
        if 'name' in kwargs:
            return FileItemResource.get_file_by_name(kwargs['name'])
        elif 'pk' in kwargs:
            return FileItemResource.get_file_items()[int(kwargs['pk'])]
        return None

    @staticmethod
    def get_file_by_name(name):
        file_items = FileItemResource.get_file_items()
        for file_item in file_items:
            if file_item.name == helpers.u_to_str(name):
                return file_item

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

    def get_object_list(self, request):
        # inner get of object list... this is where you'll need to
        # fetch the data from what ever data source
        return FileItemResource.get_file_items()

    def obj_get_list(self, request=None, **kwargs):
        # outer get of object list... this calls get_object_list and
        # could be a point at which additional filtering may be applied
        return self.get_object_list(request)

    def obj_get(self, request=None, **kwargs):
        # get one object from data source
        try:
            return FileItemResource.get_file_item(kwargs)
        except KeyError:
            raise NotFound("Object not found")

    def obj_create(self, bundle, request=None, **kwargs):
        # create a new File
        bundle.obj = FileItem()
        # full_hydrate does the heavy lifting mapping the
        # POST-ed payload key/values to object attribute/values
        bundle = self.full_hydrate(bundle)
        with open(helpers.get_filename_absolute(bundle.data[u'name']), 'w+') as uploaded_file:
            uploaded_file.write(bundle.data[u'file'])
        return bundle

    def prepend_urls(self):
        """ Add the following array of urls to the resource base urls """
        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/download%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('download'), name="api_fileitem_download"),
            url(r"^(?P<resource_name>%s)/(?P<name>[\w\d_.-]+)/download%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('download'), name="api_fileitem_download"),
            url(r"^(?P<resource_name>%s)/(?P<name>[\w\d_.-]+)/$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail_name"),
            url(r"^(?P<resource_name>%s)/(?P<id>[\d]+)/$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]

    def download(self, request, **kwargs):
        # method check to avoid bad requests
        self.method_check(request, allowed=['get'])

        response = None
        file_item = FileItemResource.get_file_item(kwargs)
        if file_item:
            filename_absolute = helpers.get_filename_absolute(file_item.name)
            if os.path.isfile(filename_absolute):
                response = serve(request, os.path.basename(filename_absolute), os.path.dirname(filename_absolute))
                response['Content-Disposition'] = 'attachment; filename="{}"'.format(os.path.basename(filename_absolute))

        if not response:
            response = self.create_response(request, {'status': 'file not found'})

        return response
