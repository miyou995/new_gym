import django_tables2 as tables
from .models import Paiement,RemunerationProf,Remuneration,Autre
from django.urls import reverse

class PiaementHTMxTable(tables.Table):
        client = tables.Column(accessor="abonnement_client__client", verbose_name="Client", orderable=True ,linkify= lambda record: record.get_url(pk=record.abonnement_client.client.pk))
        nom = tables.Column(accessor="abonnement_client__client__last_name", verbose_name="nom", orderable=True ,linkify= lambda record: record.get_url(pk=record.abonnement_client.client.pk))
        #     action = tables.TemplateColumn(
        #             '''{% include 'buttons/action.html' with object=record modal_edit="true" %}''',
        #             verbose_name='Actions',
        #             orderable=False )
        id =tables.Column( verbose_name="Reçu N°:", orderable=True )

        impression= tables.TemplateColumn(
                                        '''
                                                <a class="btn btn-primary btn-sm" 
                                                href="{% url 'transactions:impression_resu_paiement' paiement_id=record.pk  %}" 
                                                target="_blank"
                                                
                                                >Imprimer </a>
                                        '''
                                        )
        class Meta:
                fields  = (
                        'id',
                        'client',
                        'nom',
                        'abonnement_client',
                        'amount', 
                        'notes',
                        'date_creation',
                        # 'action',
                        'impression'
                )
                model = Paiement
                template_name = "tables/bootstrap_htmx.html"
                attrs = {
                "url": lambda: reverse("transactions:transaction_name"),
                "htmx_container": "#table1",
        }
        @property
        def url(self):
                return reverse("transactions:transaction_name")

        @property
        def custom_target(self):
                return "#table1"

class RemunerationProfHTMxTable(tables.Table):   
        coach = tables.Column(accessor="coach", verbose_name="coach", orderable=True ,linkify= lambda record: record.get_url(pk=record.coach.pk)) 
        action = tables.TemplateColumn(
                '''{% include 'buttons/action.html' with object=record modal_edit="true" %}''',
                verbose_name='Actions',
                orderable=False)
        
        class Meta:
                fields  = (
                        'coach',
                        'amount',
                        'notes',
                        'date_creation',
                        'action',
                )
                model = RemunerationProf
                template_name = "tables/bootstrap_htmx.html"
                attrs = {
                "url": lambda: reverse("transactions:RemunerationProfTable_name"),
                "htmx_container": "#table3",
                }
        @property
        def url(self):
                return reverse("transactions:RemunerationProfTable_name")

        @property
        def custom_target(self):
                return "#table3"


class RemunerationPersonnelHTMxTable(tables.Table):   
        nom = tables.Column(accessor="nom", verbose_name="personnel", orderable=True ,linkify= lambda record: record.get_url(pk=record.nom.pk))  
        action = tables.TemplateColumn(
                '''{% include 'buttons/action.html' with object=record modal_edit="true" %}''',
                verbose_name='Actions',
                orderable=False)
        #     def __init__(self, *args, **kwargs):
        #                 self.personnel_pk = kwargs.pop('personnel_pk', None)  # Extract the creneau_pk
        #                 super().__init__(*args, **kwargs)

        class Meta:
                fields  = (
                        'nom',
                        'amount', 
                        'notes',
                        'date_creation',
                        'action',
                )
                model = Remuneration
                template_name = "tables/bootstrap_htmx.html"
                attrs = {
                "url": lambda: reverse("transactions:RemunerationPersonnelTable_name"),
                "htmx_container": "#table2",
                }
        @property
        def url(self):
                return reverse("transactions:RemunerationPersonnelTable_name")

        @property
        def custom_target(self):
                return "#table2"


class AutreTransactionTableHTMxTable(tables.Table):   
        #     nom = tables.Column(accessor="nom", verbose_name="personnel", orderable=True ,linkify= lambda record: record.get_url())  
        action = tables.TemplateColumn(
                '''{% include 'buttons/action.html' with object=record modal_edit="true" %}''',
                verbose_name='Actions',
                orderable=False)
        
        class Meta:
                fields  = (
                        'name',
                        'amount', 
                        'notes',
                        'date_creation',
                        'action',
                )
                model = Autre
                template_name = "tables/bootstrap_htmx.html"
                attrs = {
                "url": lambda: reverse("transactions:autre_transaction_table"),
                "htmx_container": "#table4",
                }
        @property
        def url(self):
                return reverse("transactions:autre_transaction_table")

        @property
        def custom_target(self):
                return "#table4"