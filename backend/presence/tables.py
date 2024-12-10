import django_tables2 as tables
from .models import Presence
from django.urls import reverse


class PresencesHTMxTable(tables.Table):
    # tables.Column(accessor="client__id",verbose_name="carte",orderable=True , linkify=lambda record: record.client.get_view_url() if record.client else None)
    id= tables.Column(accessor="abc.client.id",verbose_name="Nom", orderable=True, linkify=lambda record:record.abc.client.get_view_url() if record.abc.client else None)
    abc = tables.Column(accessor="abc__type_abonnement", verbose_name="type d'abonnement", orderable=True )
    Creneau_date = tables.Column(accessor="creneau.day", verbose_name="Jour", orderable=True )
    reste_abc = tables.Column(accessor="abc__presence_quantity",verbose_name="Reste", orderable=True)
    prenom = tables.Column(accessor="abc__client__first_name",verbose_name="prénom", orderable=True)


    nom = tables.TemplateColumn(
        template_code='''
        {% if perms.presence.change_presence %}
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
        {% else %}
            {{  record.abc.client.last_name }}
        {% endif %}
        ''',
          verbose_name="Nom",
        orderable=True)
    def render_reste_abc(self, value, record):
        return record.abc.get_quantity_str() if record.abc.get_quantity_str() else value
    class Meta:
        fields  = (
                'id',
                'nom',
                'prenom',
                'abc',
                'Creneau_date',
                'date', 
                'hour_entree',
                'hour_sortie',
                'reste_abc',
                
        )
        model = Presence
        template_name = "tables/bootstrap_htmx.html"

