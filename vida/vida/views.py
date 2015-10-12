from django.views import generic

from vida.vida.models import Person


class IndexView(generic.ListView):

    def get_queryset(self):
        return Person.objects.order_by('created_at')


class DetailView(generic.DetailView):
    model = Person
    template_name = 'vida/person_detail.html'