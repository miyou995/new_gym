import django_tables2 as tables
from .models import Presence
from django.urls import reverse


class PresencesHTMxTable(tables.Table):

    # nom= tables.Column(accessor="abc.client.last_name",verbose_name="Nom", orderable=True)
    Creneau_activity = tables.Column(accessor="creneau.activity", verbose_name="Activité", orderable=True )
    Creneau_date = tables.Column(accessor="creneau.day", verbose_name="Jour", orderable=True )
    abc= tables.Column(accessor="abc__reste",verbose_name="Dettes", orderable=True)
    # abc= tables.Column(accessor="abc_reste",verbose_name="Dettes", orderable=True)

    nom = tables.TemplateColumn(
        template_code='''
            <a 
                href="#" 
                class="text-gray-800 text-hover-primary fs-5 fw-bold" 
                data-bs-toggle="modal" 
                data-bs-target="#kt_modal" 
                hx-get="{% url 'presence:PresenceManuelleUpdateClient' record.id %}" 
                hx-target="#kt_modal_content" 
                hx-swap="innerHTML">
                {{  record.abc.client.last_name }}
            </a>
        ''',
          verbose_name="Nom",
        orderable=True)

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

