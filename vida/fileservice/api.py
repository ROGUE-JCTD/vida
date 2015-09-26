from tastypie.authentication import BasicAuthentication
from tastypie.utils import trailing_slash
from tastypie.bundle import Bundle
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

    class Meta:
        resource_name = 'fileitem'
        object_class = FileItem
        fields = ['name']
        authentication = BasicAuthentication()

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


    # adapted this from ModelResource
    def get_resource_uri(self, bundle_or_obj):
        kwargs = {
            'resource_name': self._meta.resource_name,
        }

        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj.id # pk is referenced in ModelResource
        else:
            kwargs['pk'] = bundle_or_obj.id

        if self._meta.api_name is not None:
            kwargs['api_name'] = self._meta.api_name

        return self._build_reverse_url('api_dispatch_detail', kwargs = kwargs)

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
