import django_tables2 as tables
from planning.models import Planning
from salle_activite.models import Salle ,Activity,Door
from client.models import Maladie
from abonnement.models import Abonnement




class PlannigHTMxTable(tables.Table):
    name = tables.Column(accessor="name", verbose_name="Nom", orderable=True ,linkify= lambda record: record.get_edit_url())

    class Meta:
        fields  = (
                'name',
               
        )
        model = Planning
        template_name = "tables/bootstrap_htmx.html"
  
class SalleHTMxTable(tables.Table):
    class Meta:
        fields  = (
                'name',   
        )
        model = Salle
        template_name = "tables/bootstrap_htmx.html"

class ActivityHTMxTable(tables.Table):
    class Meta:
        fields  = (
                'name',   
                'salle',
        )
        model = Activity
        template_name = "tables/bootstrap_htmx.html"

class MaladieHTMxTable(tables.Table):
    class Meta:
        fields  = (
                'name',   
         
        )
        model = Maladie
        template_name = "tables/bootstrap_htmx.html"

class PortesHTMxTable(tables.Table):
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
    class Meta:
        fields  = (
                'name',   
                'type_of',
                'seances_quantity',
                'salles'

         
        )
        model = Abonnement
        template_name = "tables/bootstrap_htmx.html"




        