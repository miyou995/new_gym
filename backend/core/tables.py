import django_tables2 as tables
from .models import Planning
from django.urls import reverse

class PlannigHTMxTable(tables.Table):


    class Meta:
        fields  = (
                'name',
                'salle_sport',
        )
        model = Planning
        template_name = "tables/bootstrap_htmx.html"
        attrs = {
            "get_url": lambda: reverse("client:client_name"),
            "htmx_container": "#TableClient",
        }
