from django.db import models
# from client.models import Coach
from creneau.models import Creneau
from django.db.models.signals import pre_save, post_save, post_delete, pre_delete
# Create your models here.
from django.db.models import Q
from datetime import timedelta, datetime, timezone, date
from decimal import Decimal
from django.utils import timezone
from abonnement.models import AbonnementClient
from simple_history.models import HistoricalRecords
from django.conf import settings
from django.core.exceptions import ValidationError
from django.urls import reverse

FTM = '%H:%M:%S'


class PresenceManager(models.Manager):
    def get_presence(self, client_id):
        # client = Client.objects.get(id=client_id)
        presences = Presence.objects.filter(abc__client__id=client_id, hour_sortie__isnull=True)
        print('TRUEEEEEEEEEEEE', presences)
        print('client_id', client_id)
        try :
            presence = presences.last().id
        except :
            presence = False
        print('TRUEEEEEEEEEEEE', presence)
        return presence


class Presence(models.Model):
    abc         = models.ForeignKey(AbonnementClient, on_delete=models.CASCADE,related_name='presences',verbose_name='Abonnement client')
    date        = models.DateField( default=timezone.now,auto_now=False, auto_now_add=False,blank=True, null=True)
    creneau     = models.ForeignKey(Creneau, on_delete=models.CASCADE,related_name='presenses', null=True, blank=True)
    is_in_list  = models.BooleanField(default=True) # check if the person is in the list of client that should be in this creneau
    hour_entree = models.TimeField()
    hour_sortie = models.TimeField(auto_now_add=False, null=True, blank=True)
    is_in_salle = models.BooleanField(default=False)
    # remote_device = models.BooleanField(default=False)
    note        = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(verbose_name="Date de Création", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Date de dernière mise à jour", auto_now=True)
    objects = models.Manager()
    presence_manager = PresenceManager()
    history = HistoricalRecords(user_model=settings.AUTH_USER_MODEL)

    class Meta:
        ordering  = ['-created']

    def save(self, *args, **kwargs):
        # print(' Save() on Presence class ( model)')
        if not self.date:
            self.date = datetime.now().date()
        # self.full_clean()
        return super().save(*args, **kwargs)
    
    def get_time_consumed(self, sortie=None):
        today = date.today()
        now_time = datetime.now().time()
        if sortie:
            d_end = datetime.combine(today, sortie)
        else:
            d_end = datetime.combine(today, now_time)
        if self.abc.is_time_volume():
            d_start = datetime.combine(today, self.hour_entree)
            diff =  d_end - d_start 
            diff_secondes = diff.total_seconds() 
            minutes = diff_secondes / 60
            ecart = int(minutes)
        else :
            ecart = 1
        self.hour_sortie = now_time
        return ecart
    
    def get_edit_url(self):
        return reverse('presence:PresenceManuelleUpdateClient', kwargs={'pk': str(self.id)})
    
    def get_delete_url(self):
        return reverse('presence:Presence_manuelle_deleteclient', kwargs={'pk': str(self.id)})



    

    # def get_time_consumed(self, sortie=None):
    #     if not sortie :
    #         sortie = datetime.now().time()
    #     ecart = timedelta(sortie) - timedelta(self.hour_entree)
    #     print('ECART', ecart)
    #     return ecart



class PresenceCoach(models.Model):
    coach      = models.ForeignKey('client.Coach', on_delete=models.CASCADE,related_name='presencesCoach', null=True, blank=True)
    date        = models.DateField(auto_now_add=True)
    # creneau     = models.ForeignKey(Creneau, on_delete=models.CASCADE,related_name='presencesCoach', null=True, blank=True)
    hour_entree = models.TimeField(auto_now_add=False,null=True, blank=True)
    hour_sortie = models.TimeField(auto_now_add=False, null=True, blank=True)
    is_in_salle = models.BooleanField(default=False) #TODO remove this
    history = HistoricalRecords()




def presence_coach_create_signal(sender, instance, created,**kwargs):
    FTM = '%H:%M:%S'
    if created :
        current_time = datetime.now.strftime("%H:%M:%S")
        # id_coach = instance.coach.id
        # coach = Coach.objects.get(id=id_coach)
        # creneaux_actuel = Creneau.range.get_creneau()
        instance.hour_entree = current_time
        instance.save()
        # par_heur = coach.pay_per_hour 
        # entree = str(instance.hour_entree)
        # sortie = str(instance.hour_sortie)
        # duree_hour =   datetime.strptime(sortie, FTM) - datetime.strptime(entree, FTM) 
        # duree_seconde = timedelta.total_seconds(duree_hour) 
        # temps_heure = duree_seconde / 60
        # print('le total du temps passé COACH est de de !: ', par_heur)
        # # montant = instance.amount
        # # total_heures = 
        # # decimal.Decimal(str(a)

        # salaire_seance = (int(temps_heure) / 60 )  * par_heur
        # coach.salaire += Decimal(str(salaire_seance))
        # coach.save()


# def presence_coach_signal(sender, instance, **kwargs):
#     FTM = '%H:%M:%S'
#     if instance.hour_sortie:
#         id_coach = instance.coach.id
#         coach = Coach.objects.get(id=id_coach)
#         try :
#             par_heur = coach.pay_per_hour 
#             entree = str(instance.hour_entree)
#             sortie = str(instance.hour_sortie)
#             duree_hour =   datetime.strptime(sortie, FTM) - datetime.strptime(entree, FTM) 
#             duree_seconde = timedelta.total_seconds(duree_hour) 
#             temps_heure = duree_seconde / 60
#             # print('le total du temps passé COACH est de de !: ', par_heur)
#             # montant = instance.amount
#             # total_heures = 
#             # decimal.Decimal(str(a)
        
#             salaire_seance = (int(temps_heure) / 60 )  * par_heur
#             coach.salaire += Decimal(str(salaire_seance))
#             # print('le total du temps passé COACH est de de !: ', coach.salaire)

#             coach.save()
#         except :
#             coach.salaire += 0
#             coach.save()


# pre_save.connect(presence_coach_signal, sender=PresenceCoach)

# 33756.
  
# def presence_create_signal(sender, instance, created,**kwargs):
#     FTM = '%H:%M:%S'
#     if created :
#         date = instance.date
# post_save.connect(presence_create_signal, sender=Presence)
# def presence_delete_signal(sender, instance, **kwargs):
#     if instance.abc.presence_quantity :
#         print('oui', instance.abc.presence_quantity)
#         try:
#             instance.abc.presence_quantity += 1
#             instance.abc.save()
#         except:
#             pass
#     else:
#         instance.abc.presence_quantity = 0
#         instance.abc.save()

    

# post_delete.connect(presence_delete_signal, sender=Presence)


