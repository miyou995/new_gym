

from django.views.generic.base import TemplateView
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView 
from .models import Presence
from .tables import PresencesHTMxTable




class PresencesView(SingleTableMixin, FilterView):
    table_class = PresencesHTMxTable
    model = Presence
    paginate_by = 15
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
      
        return context
    def get_template_names(self):
        
        if self.request.htmx:
            template_name = "tables/product_table_partial.html"
        else:
            template_name = "presences.html" 
        return template_name 
