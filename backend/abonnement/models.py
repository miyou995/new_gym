from django.db import models
from client.models import Client
from datetime import datetime, timedelta, date
from salle_activite.models import Activity, Salle 
from creneau.models import Creneau
# Signals imports
from django.db.models.signals import post_save, pre_save


# class ManagerValidity(models.Manager):

#     def is_valid(self, abc_id):
#         abonnement = AbonnementClient.objects.get(id = abc_id)
#         abc_end_date = abonnement.end_date
#         today = date.today()
#         print('end date =', abc_end_date)
#         print('today = ', today)
#         if today < abc_end_date:
#             return True
#         else:
#             return False 
        # return True

# class AbonnementManager(models.Manager):
#     def get_queryset():
#         return Abonnement.objects.filter(actif= True)
        # return True
TYPE_ABONNEMENT = (
    ('VH', 'Volume Horaire'),
    ('OU', 'Ouvert'),
    ('SL', 'Seance limité'),
)
class Abonnement(models.Model):
    name              = models.CharField(max_length=70, verbose_name="Nom")
    price             = models.DecimalField(max_digits=15, decimal_places=0, verbose_name="prix")
    number_of_days    = models.IntegerField()# number of days
    seances_quantity  = models.IntegerField()
    salles            = models.ManyToManyField(Salle, related_name='abonnements')
    systeme_cochage   = models.BooleanField(default=False)
    actif             = models.BooleanField(default=True)
    # objects           = AbonnementManager()
    def __str__(self):
        return self.name

    def get_seances_quantity(self):
        return self.seances_quantity


class AbonnementClient(models.Model):
    start_date          = models.DateField()# number of days
    end_date            = models.DateField()# number of days
    created_date_time   = models.DateTimeField(auto_now_add=True)
    updated_date_time   = models.DateTimeField(auto_now=True)
    client              = models.ForeignKey(Client, related_name="abonnement_client", on_delete=models.CASCADE)
    type_abonnement     = models.ForeignKey(Abonnement, related_name="type_abonnement_client", on_delete=models.CASCADE)
    presence_quantity   = models.IntegerField(blank=True, null=True)
    creneaux            = models.ManyToManyField(Creneau, verbose_name="créneau", related_name='pizzas', blank=True)
    reste               = models.DecimalField(max_digits=15, decimal_places=0, verbose_name="prix", blank=True, null=True)
    archiver            = models.BooleanField(default=False)
    objects             = models.Manager()
    # validity            = ManagerValidity()

    def is_valid(self):
        today = date.today()
        if today < self.end_date:
            return True
        else:
            return False 

    def __str__(self):
        return  str(self.id)
    def get_type(self):
        return self.type_abonnement.type


# def dette_signal(sender, instance, **kwargs):
#     id_client = instance.client.id
#     client = Client.objects.get(id=id_client)
#     price = instance.type_abonnement.price
#     try:
#         client.dette += price
#     except:
#         client.dette = 0
#     client.save()

# post_save.connect(dette_signal, sender=AbonnementClient)


def abc_created_signal(sender, instance, created,**kwargs):
    if created:
        abon = instance.type_abonnement
        presence_quantity = abon.seances_quantity
        reste = abon.price
        # end_date = datetime.now().date() + timedelta(days = number_of_days)
        #  updates
        instance.reste = reste
        instance.presence_quantity = presence_quantity
        # instance.end_date = end_date
        instance.save()

post_save.connect(abc_created_signal, sender=AbonnementClient)




    # def create(self, validated_data):
    #     print('validated_data =====>', validated_data)
    #     # return AbonnementClient.objects.create(**validated_data)
    #     abon = validated_data['type_abonnement']
    #     number = Abonnement.objects.get(id = abon.id).number_of_days
    #     delta = timedelta(days = number)
    #     end_date = datetime.now().date() + delta
    #     presence_quantity = Abonnement.objects.get(id = abon.id).seances_quantity

    #     abonnement_client = AbonnementClient.objects.create(end_date=end_date,presence_quantity=presence_quantity, **validated_data)
    #     return abonnement_client


    # 0561 64 40 67 aymen bencherchali



