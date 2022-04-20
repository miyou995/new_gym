from django.db import models
from client.models import Client
from datetime import datetime, timedelta, date
from salle_activite.models import Activity, Salle 
from creneau.models import Creneau
# Signals imports
from django.db.models.signals import post_save, pre_save

class SubscriptionManager(models.Manager):
    def time_volume(self):
        return self.filter(type_abonnement__type_of=="VH")
    def free_access(self):
        return self.filter(type_abonnement__type_of=="AL")
    def fixed_sessions(self):
        return self.filter(type_abonnement__type_of=="SF")
    def free_sessions(self):
        return self.filter(type_abonnement__type_of=="SL")
    def free_access_subscription(self):
        return self.exclude(type_abonnement__type_of= "SF")
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
    ('AL', 'Accés Libre'),
    ('SF', 'Seances Fix'),
    ('SL', 'Seances Libre'),
)

class Abonnement(models.Model):
    name             = models.CharField(max_length=70, verbose_name="Nom")
    type_of          = models.CharField(choices= TYPE_ABONNEMENT, max_length=2, default='VH',verbose_name="type d'abonnement")
    price            = models.DecimalField(max_digits=15, decimal_places=0, verbose_name="prix")
    length           = models.IntegerField()# number of days
    seances_quantity = models.IntegerField( blank=True, null=True)
    salles           = models.ManyToManyField(Salle, related_name='abonnements')
    actif            = models.BooleanField(default=True)
    # objects        = AbonnementManager()
    def __str__(self):
        return self.name

    def time_volume(self):
        return True if self.type_of == "VH" else False
    def free_access(self):
        return True if self.type_of == "AL" else False
    def fixed_sessions(self):
        return True if self.type_of == "SF" else False
    def free_sessions(self):
        return True if self.type_of == "SL" else False
        
class AbonnementClient(models.Model):
    start_date          = models.DateField()# number of days
    end_date            = models.DateField()# number of days
    client              = models.ForeignKey(Client, related_name="abonnement_client", on_delete=models.PROTECT)
    type_abonnement     = models.ForeignKey(Abonnement, related_name="type_abonnement_client", on_delete=models.CASCADE)
    presence_quantity   = models.IntegerField(blank=True, null=True)
    creneaux            = models.ManyToManyField(Creneau, verbose_name="créneau", related_name='abonnements', blank=True)
    reste               = models.DecimalField(max_digits=15, decimal_places=0, verbose_name="prix", blank=True, null=True)
    archiver            = models.BooleanField(default=False)
    created_date_time   = models.DateTimeField(auto_now_add=True)
    updated_date_time   = models.DateTimeField(auto_now=True)
    objects             = models.Manager()
    # validity            = ManagerValidity()
    subscription_type   =SubscriptionManager()

    def is_time_volume(self):
        return True if self.type_abonnement.type_of == "VH" else False
    def is_free_access(self):
        return True if self.type_abonnement.type_of == "AL" else False
    def is_fixed_sessions(self):
        return True if self.type_abonnement.type_of == "SF" else False
    def is_free_sessions(self):
        return True if self.type_abonnement.type_of == "SL" else False
        
    def is_valid(self):
        today = date.today()
        if today < self.end_date:
            return True
        else:
            return False 

    def __str__(self):
        return  str(self.id)
    def get_type(self):
        return self.type_abonnement.type_of

    def get_planning(self):
        try:
            print('creneaaaau', self.creneaux.first().planning)
            return self.creneaux.first().planning
        except:
            return None

    def get_activites(self):
        activities = Activity.objects.filter(salle__abonnements__type_abonnement_client=self)
        # activites = self.type_abonnement.salles.activities
        print('les activité de cet abc ', activities)
        return activities

    def renew_abc(self):
        type_abonnement = self.type_abonnement
        delta = timedelta(days = type_abonnement.length)
        new_start_date = self.start_date
        if self.is_valid():
            self.end_date = self.end_date + delta
            self.reste += type_abonnement.price
            self.presence_quantity += type_abonnement.seances_quantity
            if self.is_time_volume():
                print("cest un abonnement de volume horaire")
                self.presence_quantity += type_abonnement.seances_quantity *60
            else:
                print("cest un abonnement de Seances")
                self.presence_quantity += type_abonnement.seances_quantity
        else:
            self.start_date =  date.today()
            self.end_date = self.start_date + delta
            self.reste += type_abonnement.price
            if self.is_time_volume():
                print("cest un abonnement de volume horaire")
                self.presence_quantity = type_abonnement.seances_quantity *60
            else:
                print("cest un abonnement de Seances")
                self.presence_quantity = type_abonnement.seances_quantity
        self.save()
        # methode creer normaleemnt rest view / la method ne marche pas !!
        




def creneau_created_signal(sender, instance, created,**kwargs):
    if created:
        # get abc that have free access VH, AL, SL - 
        abonnements = AbonnementClient.subscription_type.free_access_subscription()
        # get abc that has same activities as creneaux abonnements 
        activity = instance.activity
        for abonnement in abonnements:
            if abonnement.get_planning() == instance.planning:
                if activity in abonnement.get_activites():
                    abonnement.creneaux.add(instance)
                    abonnement.save()
        instance.save()
post_save.connect(creneau_created_signal, sender=Creneau)


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


# def abc_created_signal(sender, instance, created,**kwargs):
#     if created:
#         abon = instance.type_abonnement
#         presence_quantity = abon.seances_quantity
#         reste = abon.price
#         # end_date = datetime.now().date() + timedelta(days = length)
#         #  updates
#         instance.reste = reste
#         instance.presence_quantity = presence_quantity
#         # instance.end_date = end_date
#         instance.save()

# post_save.connect(abc_created_signal, sender=AbonnementClient)




    # def create(self, validated_data):
    #     print('validated_data =====>', validated_data)
    #     # return AbonnementClient.objects.create(**validated_data)
    #     abon = validated_data['type_abonnement']
    #     number = Abonnement.objects.get(id = abon.id).length
    #     delta = timedelta(days = number)
    #     end_date = datetime.now().date() + delta
    #     presence_quantity = Abonnement.objects.get(id = abon.id).seances_quantity

    #     abonnement_client = AbonnementClient.objects.create(end_date=end_date,presence_quantity=presence_quantity, **validated_data)
    #     return abonnement_client


    # 0561 64 40 67 aymen bencherchali



