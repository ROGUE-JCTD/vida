from django.views import generic
from tastypie.resources import ModelResource, ALL
from django.db.models import Q
from django.db.models import Max, Min
import helpers

from vida.vida.models import Person, Shelter

# class DISTScoreContextMixin(object):
#
#     @staticmethod
#     def add_dist_values_to_context():
#         context = {}
#         score_metrics = Person.objects.all().aggregate(Max('age'), Min('age'))
#         context['dist_max'] = score_metrics['age__max']
#         context['dist_min'] = score_metrics['age__min']
#
#         return context

class PersonIndexView(generic.ListView):
    model = Person
    paginate_by = 30
    queryset = Person.objects.all()
    sort_by_fields = [
        ('given_name', 'Name Ascending'),
        ('-given_name', 'Name Descending'),
        ('age', 'Age Ascending'),
        ('-age', 'Age Descending')
        ]

    search_fields = ['given_name', 'barcode']
    range_fields = ['age']

    def get_queryset(self):
        queryset = super(PersonIndexView, self).get_queryset()

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
                Q(shelter__icontains=string_val) |
                Q(barcode__exact=string_val)
            )

            if number_val:
                custom_query = (
                    (
                        Q(age__gte=number_val-10) &
                        Q(age__lte=number_val+10)
                    ) |
                    (
                        Q(barcode__exact=string_val)
                    ) |
                    Q(description__icontains=number_val) |
                    Q(notes__icontains=string_val) |
                    Q(shelter__icontains=string_val)
                )

            return custom_query

        if self.request.GET.get('q'):
            query_str = self.request.GET.get('q')
            custom_query = filter_custom_query(query_str)
            queryset = queryset.filter(custom_query)
        else:
            for field, value in self.request.GET.items():
                if value and value.lower() != 'any' and field in self.search_fields:
                    if field.lower().endswith('name'):
                        field += '__icontains'
                    queryset = queryset.filter(**{field: value})

                #range is passed as pair of comma delimited min and max values for example 12,36
                try:
                    if field in self.range_fields and value and "," in value:
                        min, max = value.split(",")
                        Min = int(min)
                        Max = int(max)
                        if (Min == 0 and Max == 100):
                            pass;
                        else:
                            if Min:
                                queryset = queryset.filter(**{field+'__gte': Min})

                            if Max:
                                queryset = queryset.filter(**{field+'__lte': Max}) #|Q(**{field+'__isnull': True}))

                except:
                    pass

        return queryset



class PersonDetailView(generic.DetailView):
    model = Person
    template_name = 'vida/person_detail.html'

class ShelterDetailView(generic.DetailView):
    model = Shelter
    template_name = 'vida/shelter_detail.html'