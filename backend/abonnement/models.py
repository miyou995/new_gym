from django.db import models
from datetime import datetime, timedelta, date
from salle_activite.models import Activity, Salle 
from creneau.models import Creneau
# Signals imports
from django.db.models.signals import post_save, pre_save
from simple_history.models import HistoricalRecords

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
        return self.exclude(type_abonnement__type_of=="SF")


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
    class Meta:
        permissions = [('can_view_history', 'Can View history')]

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
    client              = models.ForeignKey('client.Client', related_name="abonnement_client", on_delete=models.PROTECT)
    type_abonnement     = models.ForeignKey(Abonnement, related_name="type_abonnement_client", on_delete=models.CASCADE)
    presence_quantity   = models.IntegerField(blank=True, null=True)
    creneaux            = models.ManyToManyField(Creneau, verbose_name="créneau", related_name='abonnements', blank=True)
    reste               = models.DecimalField(max_digits=15, decimal_places=0, verbose_name="prix", blank=True, null=True)
    archiver            = models.BooleanField(default=False)
    created_date_time   = models.DateTimeField(auto_now_add=True)
    updated_date_time   = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()
    objects             = models.Manager()
    subscription_type   = SubscriptionManager()

    def put_archiver(self):
        self.archiver = True 
        self.actif = False 
        self.creneaux.set([]) 
        self.save()
        print("ABCCCCC DELETEEDDDD")
        return self
    def is_time_volume(self):
        return True if self.type_abonnement.type_of == "VH" else False
    def is_free_access(self):
        return True if self.type_abonnement.type_of == "AL" else False
    def is_fixed_sessions(self):
        return True if self.type_abonnement.type_of == "SF" else False
    def is_free_sessions(self):
        return True if self.type_abonnement.type_of == "SL" else False
    def get_day_index(self, day):
        if day == 'DI':
            return 6
        elif day == 'LU':
            return 0
        elif day == 'MA':
            return 1
        elif day == 'ME':
            return 2
        elif day == 'JE':
            return 3
        elif day == 'VE':
            return 4
        elif day == 'SA':
            return 5
        else:
            return False
    def get_next_date(self, given_start_date, day):
        today = date.today()
        formated_start_date = datetime.strptime(given_start_date, "%Y-%m-%d")
        weekday = formated_start_date.weekday()
        print('TODAY DE TODAY', weekday)
        the_next_date = formated_start_date + timedelta((day-weekday) % 7)
        return the_next_date

    def get_end_date(self, start_date, creneaux):
        duree = self.type_abonnement.length
        # print('get_end_date start_date => ', start_date)
        # print('get_end_date duree => ', duree)
        duree_semaine = (duree // 7) - 1 
        selected_creneau= [cre.id for cre in creneaux]
        # print('get_end_date duree_semaine => ', duree_semaine)
        dates_array = []
        formated_start_date = datetime.strptime(start_date, "%Y-%m-%d")
        # print('get_end_date formated_start_date => ', formated_start_date)
        calculated_end_date = formated_start_date + timedelta(days=duree)
        # print('get_end_date calculated_end_date 1 => ', calculated_end_date)
        if self.is_fixed_sessions():
            for creneau in creneaux :
                jour = self.get_day_index(creneau.day)
                # print('get_end_date jour  => ', jour)
                next_date = self.get_next_date(start_date, jour)
                # print('get_end_date next_date  ====> ', next_date)
                # print(f'le prochain {creneau.day} in: {jour} est le {next_date}')
                dates_array.append(next_date)
            maxed_date = max(dates_array)
            calculated_end_date = maxed_date + timedelta(weeks=duree_semaine)
            # print('get_end_date calculated_end_date 2 => ', calculated_end_date)
        return calculated_end_date



    def is_no_more_actif(self):
        today = date.today()
        if today > self.end_date:
            return True
        else:
            return False 

    def is_actif(self):
        today = date.today()
        # print('today', today)
        # print('end_date', self.end_date)
        if today <= self.end_date:
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

    def renew_abc(self, renew_start_date):
        type_abonnement = self.type_abonnement
        delta = timedelta(days = type_abonnement.length)
        creneaux = self.creneaux.all()
        creneaux_ids = self.creneaux.all().values_list('id', flat=True)
        new_end_date = self.get_end_date(renew_start_date, creneaux)
        print('the renew_start_date', renew_start_date)
        print('the new_end_date', new_end_date)
        new_start_date = renew_start_date
        self.pk = None
        self.save()
        for creneau in creneaux:
            self.creneaux.add(creneau)
        # self.creneaux.add(creneaux_ids) 
        self.end_date = new_end_date
        self.start_date = new_start_date
        self.reste = type_abonnement.price
        self.save()
        # abc_id = self.id
        return self



    def get_quantity_str(self):
        if self.is_time_volume():
            minutes = self.presence_quantity
            time = divmod(minutes, 60)
            # print('en heures', time)
            time_string = "{}H: {}M".format(time[0], time[1])
            # print('en time_string', time_string)
            return time_string
        else:
            return self.presence_quantity


    # def renew_abc(self, renew_start_date):
    #     type_abonnement = self.type_abonnement
    #     delta = timedelta(days = type_abonnement.length)
    #     new_start_date = self.start_date
    #     self.reste += type_abonnement.price
    #     if self.is_valid():
    #         self.end_date = self.end_date + delta
    #         # self.presence_quantity += type_abonnement.seances_quantity
    #         if self.is_time_volume():
    #             print("cest un abonnement de volume horaire")
    #             added = type_abonnement.seances_quantity *60
    #             print('added', added)
    #             self.presence_quantity += added
    #         else:
    #             print("cest un abonnement de Seances")
    #             added = type_abonnement.seances_quantity
    #             print('added', added)
    #             self.presence_quantity += added
    #         print("cest  self.presence_quantity ", self.presence_quantity )
            
    #         self.start_date =  date.today()
    #         self.end_date = self.start_date + delta
    #         self.reste += type_abonnement.price
    #     else:
    #         if self.is_time_volume():
    #             print("cest un abonnement de volume horaire 2")
    #             self.presence_quantity = type_abonnement.seances_quantity *60
    #         else:
    #             print("cest un abonnement de Seances 2")
    #             self.presence_quantity = type_abonnement.seances_quantity
    #     self.save()
    #     return self
        # methode creer normaleemnt rest view / la method ne marche pas !!
        




def creneau_created_signal(sender, instance, created,**kwargs):
    if created:
        # get abc that have free access VH, AL, SL - 
        abonnements = AbonnementClient.objects.all()
        # abonnements = AbonnementClient.subscription_type.free_access_subscription()
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


