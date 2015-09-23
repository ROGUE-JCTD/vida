from django.views import generic
from .models import Person


class IndexView(generic.ListView):
    template_name = 'person/index.html'

    def get_queryset(self):
        return Person.objects.order_by('created_at')[:5]


class DetailView(generic.DetailView):
    model = Person
    template_name = 'person/detail.html'


class Person(generic.DetailView):
    model = Person
    template_name = 'person/results.html'
