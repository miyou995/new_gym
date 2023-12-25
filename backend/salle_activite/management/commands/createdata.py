import faker.providers
from django.core.management.base import BaseCommand
from faker import Faker

from django.contrib.auth import get_user_model

from apps.catalogue.factories import (AtributeFactory, AtributesValueFactory,
                                      BrandFactory, CategoryBannerFactory,
                                      CategoryFactory, CategorySpecsFactory,
                                      ColorFactory, PhotoProductFactory,
                                      ProductFactory, ProductSpecsFactory,
                                      ProductTypeFactory,
                                      )
from apps.catalogue.models import *
from apps.comment.factories import CommentFactory, PhotoCommentFactory
from apps.comment.models import Comment, PhotoComment
from apps.marketing.factories import CouponFactory, DiscountFactory
from apps.marketing.models import Coupon, Discount
from apps.tenant.models import Client
from django_tenants.utils import tenant_context

# class Provider(faker.providers.BaseProvider):
#     def category(self):
#         return None
#     def products(self):


User = get_user_model()


class Command(BaseCommand):
    help = "Create fake data. you have to pass --schema=all-tenants for all tenants or the name of the tenant example --schema=demo"
    def add_arguments(self, parser):
        parser.add_argument(
            '--schema',
            action='store',
            dest='schema',
            help='Name of the tenant schema',
        )
    def handle(self, *args,**kwargs):
        schema_name = kwargs['schema']
        self.stdout.write('START handing')
        if schema_name is None:
            self.stdout.write(self.style.ERROR('Please provide a tenant schema name... schema= '))
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
                # ... the rest of your com
                # fake = Faker()
                # fake.add_provider(Provider)
                self.stdout.write('START DELETING')
                # User.objects.all().delete()
                Comment.objects.all().delete()
                PhotoComment.objects.all().delete()
                PhotoProduct.objects.all().delete()
                ProductSpecs.objects.all().delete()
                Product.objects.all().delete()
                CategoryBanner.objects.all().delete()
                Category.objects.all().delete()
                AtributesValue.objects.all().delete()
                Atribute.objects.all().delete()
                ProductType.objects.all().delete()
                Color.objects.all().delete()
                Brand.objects.all().delete()
                Coupon.objects.all().delete()
                Discount.objects.all().delete()
                # User.objects.create_superuser(
                #         # phone=cd['phone'],
                #         # address=cd['address'],
                #         email="admin@admin.com",
                #         password="admin"
                #     )
                self.stdout.write('START GENERATION')
                for _ in range(50):
                    ColorFactory()

                for _ in range(50):
                    BrandFactory()

                for _ in range(8):
                    CategoryFactory()
                    
                for _ in range(50):
                    CategoryBannerFactory()

                for _ in range(8):
                    ProductTypeFactory()

                for _ in range(15):
                    AtributeFactory()

                for _ in range(50):
                    AtributesValueFactory()
                    
                for _ in range(160):
                    ProductFactory()

                for _ in range(700):
                    PhotoProductFactory()

                for _ in range(50):
                    CategorySpecsFactory()

                for _ in range(50):
                    ProductSpecsFactory()


                for _ in range(50):
                    CouponFactory()
                for _ in range(50):
                    DiscountFactory()
                # for _ in range(50):
                #     CommentFactory()
                # for _ in range(50):
                #     PhotoCommentFactory()
                
                pt = ProductType.objects.create(name="clothes")
                at = Atribute.objects.create(name="Taille", product_type=pt)
                AtributesValue.objects.create(value="XS", atribut=at)
                AtributesValue.objects.create(value="S", atribut=at)
                AtributesValue.objects.create(value="L", atribut=at)



# class Command(BaseCommand):
#     help = "Generates test data"

#     @transaction.atomic
#     def handle(self, *args, **kwargs):
#         self.stdout.write("Deleting old data...")
#         User.objects.all().delete()
#         Thread.objects.all().delete()
#         Comment.objects.all().delete()
#         Club.objects.all().delete()
#         self.stdout.write("Creating new data...")
#         people = []
#         for _ in range(50):
#             person = UserFactory()
#             people.append(person)

#         for _ in range(10):
#             club = ClubFactory()
#             members = random.choices(people, k=8)
#             club.user.add(*members)

#         for _ in range(12):
#             creator = random.choice(people)
#             thread = ThreadFactory(creator=creator)
#             for _ in range(25):
#                 commentor = random.choice(people)
#                 CommentFactory(user=commentor, thread=thread)