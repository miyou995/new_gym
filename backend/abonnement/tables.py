import django_tables2 as tables
from django.urls import reverse

from .models import AbonnementClient


class AbonnementClientHTMxTable(tables.Table):
    id = tables.Column(
        accessor="client__id", linkify=lambda record: record.client.get_absolute_url()
    )
    created_date_time = tables.DateTimeColumn(
        format="d/m/Y", verbose_name="Date d'ajout"
    )
    is_locked = tables.BooleanColumn(verbose_name="Bloqué")

    class Meta:
        model = AbonnementClient
        template_name = "tables/bootstrap_htmx.html"
        fields = (
            "id",
            "client__last_name",
            "client__first_name",
            "client__phone",
            "type_abonnement",
            "reste",
            "is_locked",
            "created_date_time",
        )
        attrs = {
            "class": "table table-striped table-hover align-middle",
            "url": lambda: reverse("abonnement:abonnement_client"),
            "htmx_container": "#TableClient",
        }
        row_attrs = {"class": lambda record: "table-danger" if record.is_locked else ""}
