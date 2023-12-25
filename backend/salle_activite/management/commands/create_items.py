import uuid
from django.core.management.base import BaseCommand
from apps.tenant.models import Client
from django_tenants.utils import tenant_context

from apps.catalogue.models import *
from apps.inventory.models import *





class Command(BaseCommand):
    help = "Create fake warehouse items  and ProductOptions. you have to pass --schema=all-tenants for all tenants or the name of the tenant example --schema=demo"
    def add_arguments(self, parser):
        parser.add_argument(
            '--schema',
            action='store',
            dest='schema',
            help='Name of the tenant schema',
        )
    def handle(self, *args,**kwargs):
        schema_name = kwargs['schema']

        if schema_name is None:
            self.stdout.write(self.style.ERROR('Please provide a tenant schema name.'))
            return
        # Get the tenant
        if schema_name == "all-tenants":
            tenants = Client.objects.filter(schema_name=schema_name)
        else:
            try:
                tenants = Client.objects.filter(schema_name=schema_name)
            except Client.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Tenant with schema name "{schema_name}" does not exist.'))
                return
        for tenant in tenants:
            with tenant_context(tenant):
                products = Product.objects.all()
                default, _ = WareHouse.objects.get_or_create(is_default=True, is_active=True)
                if _ :
                    default.name = "default Warehouse"
                    default.save()
                for product in products:
                    ProductOptions.objects.create(product=product, reference=uuid.uuid4())

                options = ProductOptions.objects.all()
                print('OPTIONS', options)

                for option in options:
                    self.stdout.write(f"Creating WareHouseItem for option {option.id} and default location")
                    item, created = WareHouseItem.objects.get_or_create(option=option, location=default, defaults={'available': 20})
                    if not created:
                        self.stdout.write(self.style.ERROR(f"WareHouseItem for option {option.id} and default location already exists"))
