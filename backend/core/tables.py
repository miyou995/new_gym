from presence.models import Presence
import django_tables2 as tables
from planning.models import Planning
from salle_activite.models import Salle ,Activity,Door
from transaction.models import Autre, Paiement, Remuneration, RemunerationProf, Transaction
from client.models import Maladie
from abonnement.models import Abonnement
from django.urls import reverse, reverse_lazy




class PlannigHTMxTable(tables.Table):
    #  name = tables.Column(accessor="name", verbose_name="Nom", orderable=True ,linkify= lambda record: record.get_edit_url())
    name = tables.TemplateColumn(
    template_code='''
        {% if perms.planning.change_planning %}
            <a 
                href="#" 
                class="text-gray-800 text-hover-primary fs-5 fw-bold" 
                data-bs-toggle="modal" 
                data-bs-target="#kt_modal" 
                hx-get="{% url 'core:planning_update_view' record.id %}" 
                hx-target="#kt_modal_content" 
                hx-swap="innerHTML">
                {{ record.name }}
            </a>
        {% else %}
            {{ record.name }}
        {% endif %}
        ''',
        verbose_name="Nom")
    class Meta:
        fields  = (
                'name',
                "is_default"
               
        )
        model = Planning
        template_name = "tables/bootstrap_htmx.html"

    @property
    def url(self):
        return reverse("core:planning_table")

    @property
    def custom_target(self):
        return "#PlanningTable"
  
class SalleHTMxTable(tables.Table):
    name = tables.TemplateColumn(
        template_code='''
        {% if perms.salle_activite.change_salle %}
            <a 
                href="#" 
                class="text-gray-800 text-hover-primary fs-5 fw-bold" 
                data-bs-toggle="modal" 
                data-bs-target="#kt_modal" 
                hx-get="{% url 'core:salle_update_view' record.id %}" 
                hx-target="#kt_modal_content" 
                hx-swap="innerHTML">
                {{ record.name }}
            </a>
        {% else %}
            {{ record.name }}
        {% endif %}
        ''',
        verbose_name="Nom")
    class Meta:
        fields  = (
                'name',
               "is_default"
        )
        model = Salle
        template_name = "tables/bootstrap_htmx.html"

    @property
    def url(self):
        return reverse("core:salle_table")

    @property
    def custom_target(self):
        return "#SalleTable"

class ActivityHTMxTable(tables.Table):
    name = tables.TemplateColumn(
        template_code='''
        {% if perms.salle_activite.change_activity %}
            <a 
                href="#" 
                class="text-gray-800 text-hover-primary fs-5 fw-bold" 
                data-bs-toggle="modal" 
                data-bs-target="#kt_modal" 
                hx-get="{% url 'core:activite_update_view' record.id %}" 
                hx-target="#kt_modal_content" 
                hx-swap="innerHTML">
                {{ record.name }}
            </a>
        {% else %}
            {{ record.name }}
        {% endif %}
        ''',
        verbose_name="Nom")
    class Meta:
        fields  = (
                'name',   
                'salle',
        )
        model = Activity
        template_name = "tables/bootstrap_htmx.html"
    
    @property
    def url(self):
        return reverse("core:activity_table")

    @property
    def custom_target(self):
        return "#ActivityTable"

class MaladieHTMxTable(tables.Table):
    name = tables.TemplateColumn(
        template_code='''
            <a 
                href="#" 
                class="text-gray-800 text-hover-primary fs-5 fw-bold" 
                data-bs-toggle="modal" 
                data-bs-target="#kt_modal" 
                hx-get="{% url 'core:maladie_update_view' record.id %}" 
                hx-target="#kt_modal_content" 
                hx-swap="innerHTML">
                {{ record.name }}
            </a>
        ''',
        verbose_name="Nom")
    class Meta:
        fields  = (
                'name',
        )
        model = Maladie
        template_name = "tables/bootstrap_htmx.html"

    @property
    def url(self):
        return reverse("core:maladie_table")

    @property
    def custom_target(self):
        return "#MaladieTable"

class PortesHTMxTable(tables.Table):
    ip_adress = tables.TemplateColumn(
        template_code='''
            {% if perms.salle_activite.change_door %}
            <a 
                href="#" 
                class="text-gray-800 text-hover-primary fs-5 fw-bold" 
                data-bs-toggle="modal" 
                data-bs-target="#kt_modal" 
                hx-get="{% url 'core:porte_update_view' record.id %}" 
                hx-target="#kt_modal_content" 
                hx-swap="innerHTML">
                {{ record.ip_adress }}
            </a>
            {% else %}
                {{ record.ip_adress }}
            {% endif %}
        ''')
    class Meta:
        fields  = (
               'ip_adress',  
               'salle',
               'username',
               'password'
         
        )
        model = Door
        template_name = "tables/bootstrap_htmx.html"

    @property
    def url(self):
        return reverse("core:portes_table")

    @property
    def custom_target(self):
        return "#PortesTable"
  

class AbonnementHTMxTable(tables.Table):
    name = tables.TemplateColumn(
        template_code='''
            {% if perms.abonnement.change_abonnement %}
                <a 
                    href="#" 
                    class="text-gray-800 text-hover-primary fs-5 fw-bold" 
                    data-bs-toggle="modal" 
                    data-bs-target="#kt_modal" 
                    hx-get="{% url 'core:type_abonnement_update_view' record.id %}" 
                    hx-target="#kt_modal_content" 
                    hx-swap="innerHTML">
                    {{ record.name }}
                </a>
            {% else %}
                {{ record.name }}
            {% endif %}
        ''',
        verbose_name="Nom"
    )

    type_of = tables.Column(accessor="type_of", verbose_name="Type", orderable=True)
    seances_quantity = tables.Column(accessor="seances_quantity", verbose_name="Nombre de séance", orderable=True)
    salles = tables.ManyToManyColumn(accessor="salles", verbose_name="Salles", orderable=True)
    price = tables.Column( verbose_name="Prix", orderable=True)
    
    class Meta:
        model = Abonnement
        template_name = "tables/bootstrap_htmx.html"
        fields = (
            'name',   
            'type_of',
            'seances_quantity',
            'price',
            'salles',
        )

        
    @property
    def url(self):
        return reverse("core:abonnemen_table")

    @property
    def custom_target(self):
        return "#abonnementTable"


class TransactionOfTheDayTable(tables.Table):
    amount = tables.Column( verbose_name="Montant")
    type= tables.Column(empty_values=())  
    client = tables.Column(empty_values=())

    def render_client(self, record):
        if isinstance(record, Paiement):
            return record.abonnement_client.client.last_name  
        elif isinstance(record, Remuneration):
            return record.nom  
        elif isinstance(record, RemunerationProf):
            return record.coach  
        elif isinstance(record, Autre):
            return record.name  
        return ''
    def render_type(self, record):
        if isinstance(record, Paiement):
            return "Paiement client"  
        elif isinstance(record, Remuneration):
            return "Remuneration personnel"  
        elif isinstance(record, RemunerationProf):
            return "Remuneration coach"  
        elif isinstance(record, Autre):
            return "Autre"  
        return ''

    class Meta:
        model = Transaction  
        attrs = {'class': 'table'}
        fields = ['amount', 'type', 'client']  
        template_name = "tables/bootstrap_htmx.html"



# class ActuellementEnSalleTable(tables.Table):

#     Creneau_activity = tables.Column(accessor="creneau.activity.salle", verbose_name="Activité", orderable=True )
#     # abc= tables.Column(accessor="abc__reste",verbose_name="Dettes", orderable=True)

#     class Meta:
#         fields  = (
#                 'Creneau_activity',
#                 'presence',
                
#         )
#         model = Presence
#         template_name = "tables/bootstrap_htmx.html"