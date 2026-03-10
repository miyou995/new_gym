import django_tables2 as tables
from django.urls import reverse

from .models import AbonnementClient


class AbonnementClientHTMxTable(tables.Table):
    id = tables.Column(
        accessor="client__id", linkify=lambda record: record.client.get_absolute_url()
    )
    created_date_time = tables.DateTimeColumn(
        format="d/m/Y", verbose_name="Date de début"
    )
    is_locked = tables.BooleanColumn(verbose_name="Bloqué")
    presence_quantity=tables.Column( verbose_name="Reste (S/T)", orderable=True )
    reste = tables.Column(verbose_name="Reste (DA)", orderable=False)
    class Meta:
        model = AbonnementClient
        template_name = "tables/bootstrap_htmx.html"
        fields = (
            "id",
            "client__last_name",
            "client__first_name",
            "client__phone",
            "type_abonnement",
            "created_date_time",
            'presence_quantity',
            "reste",
            "is_locked",
        )
        attrs = {
            "class": "table table-striped table-hover align-middle",
            "url": lambda: reverse("abonnement:abonnement_client"),
            "htmx_container": "#TableClient",
        }
        row_attrs = {"class": lambda record: "table-danger" if record.is_locked else ""}



    def render_presence_quantity(self, value, record):
        return record.get_quantity_str() if record.get_quantity_str() else value
    