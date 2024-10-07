import django_tables2 as tables
from planning.models import Planning
from salle_activite.models import Salle ,Activity,Door
from transaction.models import Transaction
from client.models import Maladie
from abonnement.models import Abonnement
from django.urls import reverse




class PlannigHTMxTable(tables.Table):
#     name = tables.Column(accessor="name", verbose_name="Nom", orderable=True ,linkify= lambda record: record.get_edit_url())
      name = tables.TemplateColumn(
        template_code='''
            <a 
                href="#" 
                class="text-gray-800 text-hover-primary fs-5 fw-bold" 
                data-bs-toggle="modal" 
                data-bs-target="#kt_modal" 
                hx-get="{% url 'core:PlanningUpdateView' record.id %}" 
                hx-target="#kt_modal_content" 
                hx-swap="innerHTML">
                {{ record.name }}
            </a>
        ''')
      class Meta:
        fields  = (
                'name',
               
        )
        model = Planning
        template_name = "tables/bootstrap_htmx.html"
  
class SalleHTMxTable(tables.Table):
    name = tables.TemplateColumn(
        template_code='''
            <a 
                href="#" 
                class="text-gray-800 text-hover-primary fs-5 fw-bold" 
                data-bs-toggle="modal" 
                data-bs-target="#kt_modal" 
                hx-get="{% url 'core:SalleUpdateView' record.id %}" 
                hx-target="#kt_modal_content" 
                hx-swap="innerHTML">
                {{ record.name }}
            </a>
        ''')
    class Meta:
        fields  = (
                'name',
        )
        model = Salle
        template_name = "tables/bootstrap_htmx.html"

class ActivityHTMxTable(tables.Table):
    name = tables.TemplateColumn(
        template_code='''
            <a 
                href="#" 
                class="text-gray-800 text-hover-primary fs-5 fw-bold" 
                data-bs-toggle="modal" 
                data-bs-target="#kt_modal" 
                hx-get="{% url 'core:ActiviteUpdateView' record.id %}" 
                hx-target="#kt_modal_content" 
                hx-swap="innerHTML">
                {{ record.name }}
            </a>
        ''')
    class Meta:
        fields  = (
                'name',   
                'salle',
        )
        model = Activity
        template_name = "tables/bootstrap_htmx.html"

class MaladieHTMxTable(tables.Table):
    name = tables.TemplateColumn(
        template_code='''
            <a 
                href="#" 
                class="text-gray-800 text-hover-primary fs-5 fw-bold" 
                data-bs-toggle="modal" 
                data-bs-target="#kt_modal" 
                hx-get="{% url 'core:MaladieUpdateView' record.id %}" 
                hx-target="#kt_modal_content" 
                hx-swap="innerHTML">
                {{ record.name }}
            </a>
        ''')
    class Meta:
        fields  = (
                'name',
        )
        model = Maladie
        template_name = "tables/bootstrap_htmx.html"

class PortesHTMxTable(tables.Table):
    ip_adress = tables.TemplateColumn(
        template_code='''
            <a 
                href="#" 
                class="text-gray-800 text-hover-primary fs-5 fw-bold" 
                data-bs-toggle="modal" 
                data-bs-target="#kt_modal" 
                hx-get="{% url 'core:PorteUpdateView' record.id %}" 
                hx-target="#kt_modal_content" 
                hx-swap="innerHTML">
                {{ record.ip_adress }}
            </a>
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
  

class AbonnementHTMxTable(tables.Table):
    name = tables.TemplateColumn(
        template_code='''
            <a 
                href="#" 
                class="text-gray-800 text-hover-primary fs-5 fw-bold" 
                data-bs-toggle="modal" 
                data-bs-target="#kt_modal" 
                hx-get="{% url 'core:TypeAbonnementUpdateView' record.id %}" 
                hx-target="#kt_modal_content" 
                hx-swap="innerHTML">
                {{ record.name }}
            </a>
        '''
    )

    type_of = tables.Column(accessor="type_of", verbose_name="Type", orderable=True)
    seances_quantity = tables.Column(accessor="seances_quantity", verbose_name="Nombre de séance", orderable=True)
    salles = tables.ManyToManyColumn(accessor="salles", verbose_name="Salles", orderable=True)

    class Meta:
        model = Abonnement
        template_name = "tables/bootstrap_htmx.html"
        fields = (
            'name',   
            'type_of',
            'seances_quantity',
            'salles',
        )



class TransactionOfTheDayTable(tables.Table):
    class Meta:
        fields = (
            'amount',   
            'type_of_transaction',
            'name',
        )
        model = Transaction
        template_name = "tables/bootstrap_htmx.html"


        