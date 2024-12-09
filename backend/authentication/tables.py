import django_tables2 as tables
from django.db.models import F
from .models import User
from django_tables2.utils import Accessor, AttributeDict, computed_values
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


class UserHTMxTable(tables.Table):
    id = tables.Column(verbose_name="ID", orderable=True, linkify= lambda record: record.get_view_url()) #TODO add link
    name = tables.Column(verbose_name="ID", orderable=True, linkify= lambda record: record.get_view_url()) #TODO add link

    action = tables.TemplateColumn(
            '''{% include 'buttons/_actions.html' with object=record  modal_edit="true" %}''',
            verbose_name='Actions',
            orderable=False,
            # attrs={"td": {"class": "{% if forloop.last %}text-end{% endif %}"}}
        )
    # signale = tables.TemplateColumn(
    #     template_code='''
    #     <button class="btn btn-danger btn-sm signaler-btn">Signalé</button>
    #     ''',
    #     verbose_name='Signalé',
    #     orderable=False,
    # )
    class Meta:
        fields  = (
            'email',
            'name',
            'prenom',
            'phone',
            'age',
            'action',
            # 'signale'
            )
        model = User
        template_name = "tables/bootstrap_htmx.html"