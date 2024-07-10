import django_tables2 as tables
from .models import Client,Coach,Personnel
from abonnement.models import AbonnementClient
from transaction.models import Paiement,RemunerationProf
from django.urls import reverse
from creneau.models import Creneau
from presence.models import PresenceCoach


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
               'maladies',
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
    last_name = tables.Column(accessor="last_name", verbose_name="Nom", orderable=True ,linkify= lambda record: record.get_view_url())

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

# client details ------------------------------------------------------------------------------------------
class AbonnementClientHTMxTable(tables.Table):
    Séances = tables.Column(accessor="type_abonnement__seances_quantity", verbose_name="Séances", orderable=True )
    prix    =tables.Column(accessor="type_abonnement__price", verbose_name="Prix", orderable=True )


    class Meta:
        fields  = (
                'type_abonnement',
                'Séances',
                'start_date', 
                'end_date',
                'prix',
                'reste',
        )
        model = AbonnementClient
        template_name = "tables/bootstrap_htmx.html"

class PaiementHTMxTable(tables.Table):
    
    recu = tables.TemplateColumn(
            '''{% include 'buttons/action.html' with object=record modal_edit="true" %}''',
            verbose_name='Actions',
            orderable=False )

    class Meta:
        fields  = (
                'amount',
                'date_creation', 
                'abonnement_client',
                'recu',
         
        )
        model = Paiement
        template_name = "tables/bootstrap_htmx.html"


# coach details ------------------------------------------------------------------------------------------------

class CoachDetailHTMxTable(tables.Table):
#     Séances = tables.Column(accessor="type_abonnement__seances_quantity", verbose_name="Séances", orderable=True )
#     prix    =tables.Column(accessor="type_abonnement__price", verbose_name="Prix", orderable=True )


    class Meta:
        fields  = (
                'hour_start',
                'hour_finish',
                'day', 
                'activity',
                
        )
        model = Creneau
        template_name = "tables/bootstrap_htmx.html"

class VirementsHTMxTable(tables.Table):
#     Séances = tables.Column(accessor="type_abonnement__seances_quantity", verbose_name="Séances", orderable=True )
#     prix    =tables.Column(accessor="type_abonnement__price", verbose_name="Prix", orderable=True )


    class Meta:
        fields  = (
               'amount',
               'date_creation', 
                
        )
        model = RemunerationProf
        template_name = "tables/bootstrap_htmx.html"


class PresenceHTMxTable(tables.Table):

    class Meta:
        fields  = (
               'hour_entree',
               'hour_sortie',
               'date' 
                
        )
        model = PresenceCoach
        template_name = "tables/bootstrap_htmx.html"
