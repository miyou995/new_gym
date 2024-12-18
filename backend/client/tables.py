import django_tables2 as tables
from .models import Client,Coach,Personnel
from abonnement.models import AbonnementClient
from transaction.models import Paiement,RemunerationProf
from django.urls import reverse
from creneau.models import Creneau
from presence.models import PresenceCoach,Presence


class ClientHTMxTable(tables.Table):
    carte = tables.Column(accessor="carte", verbose_name="carte", orderable=True ,linkify= lambda record: record.get_view_url())
    id = tables.Column(accessor="id", verbose_name="ID", orderable=True ,linkify= lambda record: record.get_view_url())
    last_name = tables.Column(accessor="last_name", verbose_name="Nom", orderable=True ,linkify= lambda record: record.get_view_url())
    first_name = tables.Column(accessor="first_name", orderable=True ,linkify= lambda record: record.get_view_url())
    action = tables.TemplateColumn(
            '''{% include 'buttons/action.html' with object=record modal_edit="true" %}''',
            verbose_name='Actions',
            orderable=False )

    class Meta:
        fields  = (
                'carte',
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
            "class": "table table-striped",
            "url": lambda: reverse("client:client_name"),
            "htmx_container": "#TableClient",
        }

class CoachHTMxTable(tables.Table):
    last_name = tables.Column(accessor="last_name", verbose_name="Nom", orderable=True ,linkify= lambda record: record.get_view_url())
    first_name = tables.Column(accessor="first_name", verbose_name="Prénom", orderable=True ,linkify= lambda record: record.get_view_url())

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
        attrs = {
            "class": "table table-striped",
            "url": lambda: reverse("client:coach_name"),
            "htmx_container": "#TableCoach",
        }
        template_name = "tables/bootstrap_htmx.html"


class PersonnelHTMxTable(tables.Table):
    last_name = tables.Column(accessor="last_name", verbose_name="Nom", orderable=True ,linkify= lambda record: record.get_view_url())
    first_name = tables.Column(accessor="first_name", verbose_name="Prénom", orderable=True ,linkify= lambda record: record.get_view_url())
    action = tables.TemplateColumn(
            '''{% include 'buttons/action.html' with object=record modal_edit="true" %}''',
            verbose_name='Actions',
            orderable=False )

    class Meta:
        fields = (
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
            "url": lambda: reverse("client:personnels_name"),
            "htmx_container": "#TablePersonnel",
        }

# client details ------------------------------------------------------------------------------------------
class AbonnementClientHTMxTable(tables.Table):
#     Séances = tables.Column(accessor="type_abonnement__seances_quantity", verbose_name="Séances", orderable=True )
    presence_quantity=tables.Column( verbose_name="Reste (S/T)", orderable=True )
    start_date =tables.Column( verbose_name="Début date", orderable=True )
    end_date =tables.Column( verbose_name="Fin date", orderable=True )
    type_abonnement = tables.TemplateColumn(
        template_code='''
            {% if perms.abonnement.change_abonnementclient %}
            <a 
                href="#" 
                class="text-gray-800 text-hover-primary fs-5 fw-bold" 
                data-bs-toggle="modal" 
                data-bs-target="#kt_modal" 
                hx-get="{% url 'abonnement:retreive_abc'  record.id  %}" 
                hx-target="#kt_modal_content" 
                hx-swap="innerHTML">
                {{ record.type_abonnement }}      
            </a>      
            {% else %}
                {{ record.type_abonnement }}      
            {% endif %}
        ''')
    reste = tables.TemplateColumn(
        verbose_name="Reste (DA)",
        template_code='''
                {% if record.reste == 0 %}
                <span style="color: green;">payé</span>
                {% else %}
                <span style="color: red;">{{ record.reste }}</span>
                {% endif %}
    '''
    )
    def __init__(self, *args, **kwargs):
        self.abonnement_client_pk = kwargs.pop('abonnement_client_pk', None)  # Extract the creneau_pk
        super().__init__(*args, **kwargs)

    def render_presence_quantity(self, value, record):
        return record.get_quantity_str() if record.get_quantity_str() else value
    class Meta:
        fields  = (
                'type_abonnement',
                'presence_quantity',
                'reste',
                'start_date',
                'end_date',
        )
        model = AbonnementClient
        template_name = "tables/bootstrap_htmx.html"
        row_attrs = {
            'class': lambda record: 'table-danger' if record.blocking_date else ''
        }

    @property
    def url(self):
        if self.abonnement_client_pk is not None:
            return reverse("client:client_detail", kwargs={"pk": self.abonnement_client_pk})
        return None
    @property
    def custom_target(self):
        return "#AbonnementClientTable"

class PaiementHTMxTable(tables.Table):
    
    # recu = tables.TemplateColumn(
    #         '''{% include 'buttons/action.html' with object=record modal_edit="true" %}''',
    #         verbose_name='Actions',
    #         orderable=False )
    
    id =tables.Column( verbose_name="N°:", orderable=True )
    amount =tables.Column( verbose_name="Versement(DA)", orderable=True )
    date_creation =tables.Column( verbose_name="date", orderable=True )
    abonnement_client =tables.Column( verbose_name="abonnement", orderable=True )
    
    impression= tables.TemplateColumn(
                                '''
                                        <a class="btn btn-primary btn-sm" 
                                        href="{% url 'transactions:impression_resu_paiement' paiement_id=record.pk  %}" 
                                        target="_blank"
                                        
                                        >Imprimer </a>
                                '''
                                )
    
    def __init__(self, *args, **kwargs):
        self.abonnement_client_pk = kwargs.pop('abonnement_client_pk', None)  # Extract the creneau_pk
        super().__init__(*args, **kwargs)

    class Meta:
        fields  = (
                'id',
                'amount',
                'date_creation', 
                'abonnement_client',
                # 'recu',
                'impression'
         
        )
        model = Paiement
        template_name = "tables/bootstrap_htmx.html"
    
    @property
    def url(self):
        if self.abonnement_client_pk is not None:
            return reverse("client:paiement_client_detail", kwargs={"pk": self.abonnement_client_pk})
        return None
    @property
    def custom_target(self):
        return "#PaiementsTable"

class PresenceClientHTMxTable(tables.Table):
    
    creneau__activity = tables.Column(verbose_name = "Activité")
    Action = tables.TemplateColumn(
            '''{% include 'buttons/action.html' with object=record modal_edit="true" %}''',
            verbose_name='Actions',
            orderable=False )
    def __init__(self, *args, **kwargs):
        self.abonnement_client_pk = kwargs.pop('abonnement_client_pk', None)  # Extract the creneau_pk
        super().__init__(*args, **kwargs)

    class Meta:
        fields  = (
                'hour_entree',
                'hour_sortie', 
                'date',
                'creneau__activity',
                'Action'
         
        )
        model = Presence
        template_name = "tables/bootstrap_htmx.html"

    @property
    def url(self):
        if self.abonnement_client_pk is not None:
            return reverse("client:presence_client_detail", kwargs={"pk": self.abonnement_client_pk})
        return None
    @property
    def custom_target(self):
        return "#PresenceTable"



# coach details ------------------------------------------------------------------------------------------------

class CoachDetailHTMxTable(tables.Table):
#     Séances = tables.Column(accessor="type_abonnement__seances_quantity", verbose_name="Séances", orderable=True )
#     prix    =tables.Column(accessor="type_abonnement__price", verbose_name="Prix", orderable=True )

    def __init__(self, *args, **kwargs):
        self.coach_pk = kwargs.pop('coach_pk', None)  # Extract the creneau_pk
        super().__init__(*args, **kwargs)

    class Meta:
        fields  = (
                'hour_start',
                'hour_finish',
                'day', 
                'activity',
                
        )
        model = Creneau
        template_name = "tables/bootstrap_htmx.html"

    @property
    def url(self):
        if self.coach_pk is not None:
            return reverse("client:coach_detail", kwargs={"pk": self.coach_pk})
        return None
    @property
    def custom_target(self):
        return "#CreneauxTable"


class VirementsHTMxTable(tables.Table):
#     Séances = tables.Column(accessor="type_abonnement__seances_quantity", verbose_name="Séances", orderable=True )
#     prix    =tables.Column(accessor="type_abonnement__price", verbose_name="Prix", orderable=True )
    def __init__(self, *args, **kwargs):
        self.coach_pk = kwargs.pop('coach_pk', None)  
        super().__init__(*args, **kwargs)

    class Meta:
        fields  = (
               'amount',
               'date_creation', 
        )
        model = RemunerationProf
        template_name = "tables/bootstrap_htmx.html"

    @property
    def url(self):
        if self.coach_pk is not None:
            return reverse("client:virements_coach_detail", kwargs={"pk": self.coach_pk})
        return None
    @property
    def custom_target(self):
        return "#VirementsTable"

class PresenceCoachHTMxTable(tables.Table):

    def __init__(self, *args, **kwargs):
        self.coach_pk = kwargs.pop('coach_pk', None)  
        super().__init__(*args, **kwargs)
        
    class Meta:
        fields  = (
               'hour_entree',
               'hour_sortie',
               'date' 
                
        )
    
        model = PresenceCoach
        template_name = "tables/bootstrap_htmx.html"

    @property
    def url(self):
        if self.coach_pk is not None:
            return reverse("client:presence_coach_detail", kwargs={"pk": self.coach_pk})
        return None
    @property
    def custom_target(self):
        return "#PresenceTable"