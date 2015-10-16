from django.views import generic
from tastypie.resources import ModelResource, ALL
from django.db.models import Q
import helpers

from vida.vida.models import Person


class IndexView(generic.ListView):
    model = Person
    paginate_by = 30
    queryset = Person.objects.all()
    sort_by_fields = [
        ('name', 'Name Ascending'),
        ('-name', 'Name Descending')
        ]

    search_fields = ['name', 'address', 'city', 'state']
    range_fields = ['age', 'something_else']

    def get_queryset(self):
        queryset = super(IndexView, self).get_queryset()

        query_str = None
        def filter_custom_query(url_args):
            string_val = None
            number_val = None
            try:
                string_val = url_args

                if helpers.is_int_str(string_val):
                    number_val = int(string_val)
            except KeyError:
                return None

            custom_query = (
                Q(family_name__icontains=string_val) |
                Q(given_name__icontains=string_val) |
                Q(mothers_given_name__icontains=string_val) |
                Q(fathers_given_name__icontains=string_val) |
                Q(description__icontains=string_val) |
                Q(notes__icontains=string_val) |
                Q(shelter__icontains=string_val)
            )

            if number_val:
                custom_query = (
                    (
                        Q(age__gte=number_val-10) &
                        Q(age__lte=number_val+10)
                    ) |
                    (
                        Q(barcode__exact=number_val)
                    ) |
                    Q(description__icontains=number_val) |
                    Q(notes__icontains=string_val) |
                    Q(shelter__icontains=string_val)
                )

            return custom_query

        if self.request.GET.get('q'):
            query_str = self.request.GET.get('q')
            custom_query = filter_custom_query(query_str)
            return queryset.filter(custom_query)

        return queryset



class DetailView(generic.DetailView):
    model = Person
    template_name = 'vida/person_detail.html'