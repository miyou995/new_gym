import django_tables2 as tables
from .models import Presence
from django.urls import reverse


class PresencesHTMxTable(tables.Table):

    Creneau_activity = tables.Column(accessor="creneau_activity", verbose_name="Activité", orderable=True )
    Creneau_date = tables.Column(accessor="creneau_date", verbose_name="Jour", orderable=True )
    abc= tables.Column(accessor="abc__reste",verbose_name="Dettes", orderable=True)
    nom= tables.Column(accessor="abc.client.last_name",verbose_name="Nom", orderable=True)
    # abc= tables.Column(accessor="abc_reste",verbose_name="Dettes", orderable=True)

    class Meta:
        fields  = (
                'id',
                'nom',
                'Creneau_activity',
                'date', 
                'Creneau_date',
                'hour_entree',
                'hour_sortie',
                'notes',
                'abc',
                
        )
        model = Presence
        template_name = "tables/bootstrap_htmx.html"
        # attrs = {
        #     "get_url": lambda: reverse("client:client_name"),
        #     "htmx_container": "#TableClient",
        # }
