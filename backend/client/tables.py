import django_tables2 as tables
from .models import Client,Coach,Personnel
from django.urls import reverse


class ClientHTMxTable(tables.Table):
    last_name = tables.Column(accessor="last_name", verbose_name="Nom", orderable=True ,linkify= lambda record: record.get_view_url())
    action = tables.TemplateColumn(
            '''{% include 'buttons/action.html' with object=record modal_edit="true" %}''',
            verbose_name='Actions',
            orderable=False )

    class Meta:
        fields  = (
                'id',
                'last_name',
                'first_name', 
                'phone',
                'notes',
                'date_added',
                'action',
        )
        model = Client
        template_name = "tables/bootstrap_htmx.html"
        attrs = {
            "get_url": lambda: reverse("client:client_name"),
            "htmx_container": "#TableClient",
        }


class CoachHTMxTable(tables.Table):
    # client = tables.Column(accessor="abonnement_client__client", verbose_name="Client", orderable=True ,linkify= lambda record: record.get_url())
#     last_name = tables.Column(accessor="last_name", verbose_name="Nom", orderable=True ,linkify= lambda record: record.get_view_url())

    action = tables.TemplateColumn(
            '''{% include 'buttons/action.html' with object=record modal_edit="true" %}''',
            verbose_name='Actions',
            orderable=False )

    class Meta:
        fields  = (
            
                'last_name',
                'first_name', 
                'phone',
                'note',
                'salaire',
                'date_added',
                'action',
        )
        model = Coach
        template_name = "tables/bootstrap_htmx.html"
        attrs = {
            "get_url": lambda: reverse("client:coach_name"),
            "htmx_container": "#TableCoach",
        }


class PersonnelHTMxTable(tables.Table):
    # client = tables.Column(accessor="abonnement_client__client", verbose_name="Client", orderable=True ,linkify= lambda record: record.get_url())
    #last_name = tables.Column(accessor="last_name", verbose_name="Nom", orderable=True ,linkify= lambda record: record.get_view_url())
    action = tables.TemplateColumn(
            '''{% include 'buttons/action.html' with object=record modal_edit="true" %}''',
            verbose_name='Actions',
            orderable=False )

    class Meta:
        fields  = (
                'last_name',
                'first_name', 
                'phone',
                'function',
                'date_added',
                'action',
        )
        model = Personnel
        template_name = "tables/bootstrap_htmx.html"
        attrs = {
            "get_url": lambda: reverse("client:personnels_name"),
            "htmx_container": "#TablePersonnel",
        }