import django_tables2 as tables
from abonnement.models import AbonnementClient

class AbonnementClientHTMxTable(tables.Table):
#     Séances = tables.Column(accessor="type_abonnement__seances_quantity", verbose_name="Séances", orderable=True )
    telephne = tables.Column(accessor="client__phone",verbose_name="Téléphone", orderable=True )
    Nom_Prenom = tables.Column(accessor="client__last_name",verbose_name="Nom et Prénom" , orderable=True )


    class Meta:
        fields  = (
                'id',
                'Nom_Prenom',
                'telephne',
                'type_abonnement',
                'end_date',
                'reste',
        )
        model = AbonnementClient
        template_name = "tables/bootstrap_htmx.html"