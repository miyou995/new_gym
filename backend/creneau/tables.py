import django_tables2 as tables
from abonnement.models import AbonnementClient
from django.urls import reverse


class AbonnementClientHTMxTable(tables.Table):
#     Séances = tables.Column(accessor="type_abonnement__seances_quantity", verbose_name="Séances", orderable=True )
    client_id =tables.Column(accessor="client__id",verbose_name="carte",orderable=True , linkify=lambda record: record.client.get_view_url() if record.client else None)
    telephne = tables.Column(accessor="client__phone",verbose_name="Téléphone", orderable=True )
    Nom_Prenom = tables.Column(accessor="client__last_name",verbose_name="Nom et Prénom" , orderable=True )

    def __init__(self, *args, **kwargs):
        self.creneau_pk = kwargs.pop('creneau_pk', None)  # Extract the creneau_pk
        super().__init__(*args, **kwargs)
        
    class Meta:
        fields  = (
                'client_id',
                'Nom_Prenom',
                'telephne',
                'type_abonnement',
                'end_date',
                'reste',
        )
    
        model = AbonnementClient
        template_name = "tables/bootstrap_htmx.html"
        # attrs = {
        #     "url": "helloooooo",
        #     "get_url": lambda: reverse("creneau:abonnements_par_creneau", kwargs={"pk": record.pk}),
        #     "htmx_container": "#AbonnementParCreneau",
        # }
    @property
    def url(self):
        if self.creneau_pk is not None:
            return reverse("creneau:abonnements_par_creneau", kwargs={"pk": self.creneau_pk})
        return None
