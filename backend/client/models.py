
from django.db import models
from django.urls import reverse
from creneau.models import Creneau
from django.template.defaultfilters import slugify
from django.db import models
from django.db.models import Sum
from simple_history.models import HistoricalRecords
from django.db.models.signals import post_save, pre_save
from abonnement.models import AbonnementClient
from presence.models import Presence
from salle_activite.models import Salle, Door
from datetime import datetime, timedelta, date
from django.db import transaction
from django.utils import timezone
from .tasks import register_user
from django.utils.translation import gettext as _
from presence.models import PresenceCoach


from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
import threading

lock = threading.Lock()
import logging
logger = logging.getLogger(__name__)
FTM = '%H:%M:%S'

# Create your models here.
class AbonnementManager(models.Manager):
    def get_abonnement(self, client_id):
        client = Client.objects.get(id=client_id)
        abon = client.abonnement_client.all()
        # print('abonabonabonabon======>', abon)
        return abon

class PresenceManager(models.Manager):
    def get_last_presence(self, coach_id):
        coach = Coach.objects.get(id=coach_id)
        try :
            presence = coach.presencesCoach.filter(is_in_salle=True).last().id
            # print(presence, ' JJJJJJJJJJJJJJJJJJJJJJ')
            return presence
        except:
            presence = False
            return presence


CIVILITY_CHOICES = (
    ('MLL', 'Mlle'),
    ('MME', 'Mme'),
    ('MR', 'Mr')
)

BLOOD_CHOICES = (
    ('A-', 'A-'),
    ('A+', 'A+'),
    ('B-', 'B-'),
    ('B+', 'B+'),
    ('O-', 'O-'),
    ('O+', 'O+'),
    ('AB-', 'AB-'),
    ('AB+', 'AB+'),
)

STATE_CHOICES = (
    ('A', 'Active'),
    ('S', 'Suspendue'),
    ('N', 'Non active'),
)

# def generate_pk():
class Maladie(models.Model):
    name = models.CharField(max_length=150,blank=True, null=True)
    # client = models.ForeignKey(Client, related_name="maladies", on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.name
    
    def get_delete_url(self):
        return reverse('core:MaladieDeleteView', kwargs={'pk': str(self.id)})
    
    class Meta:
        verbose_name = 'Maladie'
        verbose_name_plural = 'Maladies'

class Client(models.Model):
    id          = models.CharField(max_length=50, primary_key=True)
    carte       = models.CharField(max_length=100, unique=True, blank=True, null=True)
    hex_card    = models.CharField(max_length=100, unique=True, blank=True, null=True)
    last_name   = models.CharField(max_length=50, verbose_name='Nom',blank=True, null=True)
    first_name  = models.CharField(max_length=50, verbose_name='Prénom')
    civility    = models.CharField(choices=CIVILITY_CHOICES , max_length=3, default='MME', verbose_name='Civilité', blank=True, null=True)
    adress      = models.CharField(max_length=200, verbose_name='Adresse', blank=True, null=True)
    picture     = models.ImageField(upload_to='photos', blank=True, null=True)
    phone       = models.CharField(max_length=22, verbose_name='Téléphone', blank=True, null=True)
    email       = models.CharField(max_length=50, verbose_name='E-mail',blank=True, null=True)
    nationality = models.CharField(max_length=50, verbose_name='Nationalité', blank=True, null=True)
    birth_date  = models.DateField(max_length=50, verbose_name='Date de naissance', blank=True, null=True)
    blood       = models.CharField(choices=BLOOD_CHOICES , max_length=3, verbose_name='Groupe sanguin')
    date_added  = models.DateField(auto_now_add=True)
    created     = models.DateTimeField(verbose_name='Date de Création',  auto_now_add=True)
    profession  = models.CharField(max_length=50, blank=True, null=True)
    updated     = models.DateTimeField(verbose_name='Date de dernière mise à jour',  auto_now=True)
    note        = models.TextField(blank=True, null=True)
    dette       = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True,default=0)
    is_on_salle = models.BooleanField(default=False)
    maladies    = models.ManyToManyField(Maladie,blank=True)
    # date_added  = models.DateTimeField(auto_now_add=True, verbose_name='Date d\'inscription')
    # state       = models.CharField(choices=STATE_CHOICES , max_length=3, verbose_name='Etat', blank=True, null=True)
    dette_assurance      = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True,default=0)
    fin_assurance       = models.DateField(max_length=50, null=True, blank=True)
    objects     = models.Manager()
    abonnement_manager = AbonnementManager()
    history = HistoricalRecords()

    def __init__(self, *args, **kwargs):
        super(Client, self).__init__(*args, **kwargs)
        # self._old_picture = self.picture

    def __str__(self):
        return str(self.id)
    
    def get_picture_url(self):
        if self.picture and hasattr(self.picture, 'url'):
            return self.picture.url

    # def generate_thumbnail(self, picture, picture_name):
    #     THUMBNAIL_SIZE = (250, 360)
    #     image = Image.open(picture)
    #     image = image.convert("RGB")
    #     image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)
    #     temp_thumb = BytesIO()
    #     image.save(temp_thumb, "JPEG")
    #     temp_thumb.seek(0)
    #     # set save=False, otherwise it will run in an infinite loop
    #     self.picture.save(self.picture.name,ContentFile(temp_thumb.read()),save=False)
    #     print('DONE')
    #     temp_thumb.close()

    # def generate_thumbnail(self, picture, picture_name):
    #     from django.core.files import File
    #     THUMBNAIL_SIZE = (250, 360)
    #     image = Image.open(picture)
    #     image = image.convert("RGB")
    #     image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)
    #     thumb_io = BytesIO()
    #     temp_thumb.seek(0)
    #     image.save(temp_thumb, format='JPEG')
    #     thumb_file = File(thumb_io, name=picture_name)
    #     insstance.thumbnail.save(instance.fichier.name,ContentFile(temp_thumb.read()),save=False)
    #     temp_thumb.close()
    #     self.picture.save(picture_name, thumb_file, save=False)
    #     print('IMAGE RESIZED')
    #     return image

        # set save=False, otherwise it will run in an infinite loop
        # picture.save(instance.picture.name,ContentFile(temp_thumb.read()),save=False)
    # C0
    
    # def save(self, *args, **kwargs):
    #     if self._old_picture != self.picture:
    #         self.generate_thumbnail(self.picture, self.picture.name)
    #         print('yess changed picturename', self.picture.name)
    #         print('yess changed picture url', self.picture.url)
    #         logger.warning('yess changed picture url-{}'.format(str(self.picture.url)))
    #         register_user.delay(self.last_name, self.id, self.picture.name)
    #     else:
    #         logger.warning('picture not changed photo url-{}'.format(str(self.id)))
    #         print('picture not changed')
    #     if not self.id:
    #         try :
    #             # print('clientsd==> ', timezone.now())
    #             last_id = Client.objects.latest('created').id
    #             print('yesssss last id = ', last_id)
    #             number = int(last_id[1::])+1
    #             print('the number', number)     
    #             result  = str(number).zfill(4)
    #             print('the result', result)     
    #             the_id = f'C{result}'   
    #             print('the id', the_id)   
    #             self.id = the_id
    #             if self.picture:  
    #                 self.generate_thumbnail(self.picture, self.picture.name)
    #                 register_user.delay(self.last_name, the_id, self.picture.name)
    #                 print('yess changed picturename', self.picture.name)
    #                 print('yess changed picturename', self.picture.name)
    #                 print('yess changed picture url', self.picture.url)
    #                 print('yess changed picturename', self.picture.name)
    #         except Exception as e:
    #             print('THE EXCEPTION ON save client', e)
    #             logger.warning('THE EXCEPTION ON save client-{}'.format(str(e)))
    #             self.id = "C0001"

    #     if self.carte:
    #         # old_carte = self.carte
    #         # print('old_carte', old_carte) 
    #         int_carte = int(self.carte)
    #         str_carte = str(int_carte)
    #         print('carte', str_carte) 
    #         new_int_carte =  int(str_carte)
    #         hex_card = hex(new_int_carte)
    #         deleted_x = hex_card.replace('0x', '')
    #         self.hex_card = deleted_x.upper().zfill(8)
    #         print('deleted_x', deleted_x) 
    #         print(' hex_card', self.hex_card) 
    #     return super().save(*args, **kwargs)
    
    def full_name(self):
        return str(self.last_name)+ " " +str(self.first_name)

    def get_view_url(self):
        return reverse("client:client_detail",kwargs={'pk': str(self.id)})
    
    def get_edit_url(self):
        return reverse('client:client_update', kwargs={'pk': str(self.id)})

    def get_delete_url(self):
        return reverse('client:client_delete', kwargs={'pk': str(self.id)})


    def remove_duplicate(self):
        presences = Presence.objects.filter(abc__client=self, hour_sortie__isnull=True)
        logger.warning('remove_duplicated presences ================> {}'.format(str(self.carte)))
        if presences:
            first_presence = presences.first()
            presences.exclude(pk=first_presence.pk).delete()

    def auto_presence(self, door_ip=None):
        logger.warning('Client requested Door Auth ===> {}'.format(str(self.id)))

        FTM = '%H:%M:%S'
        erreur = {"level": "error", "message": "Ce client n'a pas accés maintenant"}
        sortie = {"level": "success", "message": f"la sortie de {self.id} a été éffectué Avec Succée"}
        entree = {"level": "success", "message": f"Accés autoriser pour {self.id}"}
        current_time = datetime.now().strftime("%H:%M:%S")
        client = self
        presence_sortie= self.init_output()
        if presence_sortie:
            print('YESS SORTIEEE')
            return sortie
        # client.has_permission()
        creneaux = Creneau.range.get_creneaux_of_day().filter(abonnements__client=client).distinct()
        # print('Les creneaux of client=====>',Creneau.objects.filter(abonnements__client=client))
        print('creneaux du Today client=====>', creneaux)
        logger.warning('LOGLes creneaux du Today client=====-{}'.format(str(creneaux)))
        if len(creneaux) :
            dur_ref_time_format = abs(datetime.strptime(str(creneaux[0].hour_start), FTM) - datetime.strptime(current_time, FTM))
            dur_ref= timedelta.total_seconds(dur_ref_time_format) 
            cren_ref = creneaux[0]
            for cr in creneaux:
                start = str(cr.hour_start)
                print('heure de début', start)
                temps = abs(datetime.strptime(start, FTM) - datetime.strptime(current_time, FTM))
                duree_seconde = timedelta.total_seconds(temps) 
                if dur_ref > duree_seconde:
                    dur_ref = duree_seconde
                    cren_ref = cr
            abon_list = AbonnementClient.objects.filter(client = client, end_date__gte=date.today(), archiver = False ).order_by('-presence_quantity')
            if not abon_list:
                # raise serializers.ValidationError("l'adherant n'est pas inscrit aujourd'hui")
                print("*******l'adherant n'est pas inscrit aujourd'hui**********")
                return "erreur"
            
            abonnement = abon_list.filter(type_abonnement__type_of="SL").first()
            # If no non-free session is found, get the first session regardless of its type
            if not abonnement:
                abonnement = abon_list.first()
            print('ABONNEMENT<<<<<<<<<<>>>>>>>>>>>>>>>>',abonnement.get_type())
            print('ABONNEMENT is valid<<<<<<<<<<>>>>>>>>>>>>>>>>',abonnement.is_valid())
            print('ABONNEMENT presence qnt<<<<<<<<<<>>>>>>>>>>>>>>>>',abonnement.presence_quantity)

            if abonnement.is_valid() and abonnement.is_time_volume():
                print('IM HEEERE LOG ABONNEMENT==== TIME VOLUUUPME', abonnement.is_time_volume())
                Presence.objects.create(abc= abonnement, creneau= cren_ref,  hour_entree=current_time )
                return entree
            elif abonnement.is_valid() and abonnement.presence_quantity > 0:
                Presence.objects.create(abc= abonnement, creneau= cren_ref,  hour_entree=current_time )
                if abonnement.is_fixed_sessions() or abonnement.is_free_sessions():
                    abonnement.presence_quantity -= 1
                abonnement.save()
                return entree
            else:
                logger.warning('LOG abonnement.presence_quantity=====> {}'.format(str(abonnement.presence_quantity)))
                logger.warning('LOG ABONNEMENT=====-{}'.format(str(abonnement)))
                logger.warning('LOG ABONNEMENT TYPE=====-{}'.format(str(abonnement.type_abonnement.type_of)))
                return "erreur"
        else:
            print("*******l'adherant n'est pas inscrit aujourd'hui pas de abc **********")

            return "erreur"
            # messages.error(self.request, "l'adherant n'est pas inscrit aujourd'hui")
            # # raise serializers.ValidationError("l'adherant n'est pas inscrit aujourd'hui")
            # return self
        
        
    def init_output(self,  exit_hour=None):
        presences = Presence.objects.select_for_update().filter(abc__client=self, hour_sortie__isnull=True)
        with transaction.atomic():
            presence = presences.first()
            current_time = datetime.now().strftime("%H:%M:%S")
            if exit_hour:
                current_time = exit_hour
            if not presence:
                """ ecart + de 10 seconde"""
                return False
                
            logger.warning('LA PRESENCE de{}'.format(str(self.id)))
            presence_time = presence.hour_entree
            ecart = abs(datetime.strptime(current_time, FTM) - datetime.strptime(str(presence_time), FTM))
            time_diff_seconds = timedelta.total_seconds(ecart)
            if int(time_diff_seconds) <= 2:
                logger.warning('SORTIE COULD NOT BE done  ================> ')
                return False
            else:
                presence.hour_sortie = current_time
                logger.warning('SORTIE AUTORISEE ================> {}'.format(str(presence.hour_sortie)))
                presence.save()
                abc = presence.abc
                if abc.is_time_volume():
                    ecart = presence.get_time_consumed() 
                    print('ecart presence>>>>', ecart)
                    abc.presence_quantity -= ecart 
                    abc.save()
                print('la sorite--------------- ', presence.hour_sortie)
                logger.warning('la sorite--------------- {}'.format(str(presence.hour_sortie)))
                return True

    def get_access_permission(self, door_ip=None):
        logger.warning('Client requested Door Auth ===> {}'.format(str(self.id)))
        presences = Presence.objects.filter(abc__client=self, hour_sortie__isnull=True)
        print('Nombre de presence en cours=>', presences)
        logger.warning('Nombre de presence en cours=> {}'.format(str(presences.count())))
        current_time = datetime.now().strftime("%H:%M:%S")
        # the problem is that it doesn't turn the client is_on_salle to True on entering we can try to make comparison here if it less than 10 s we directly return False
        if presences:
            logger.warning('MY presence presences=> {}'.format(str(presences)))
            sortie = self.init_output()
            if not sortie: # if sortie is false this mean that the client passed the card on an interval < 10 secondes
                logger.warning('sortie??   should be false => {}'.format(str(sortie)))
                return False
            self.save()
            return sortie
        logger.warning('check for presence creation => ')
        door = Door.objects.filter(ip_adress=door_ip).first()
        salle = door.salle

        print('Adress IP', door_ip)
        print('SAlle ', salle)

        abonnements_actives = AbonnementClient.subscription.active_subscription()
        abonnement_client = abonnements_actives.filter(client=self, type_abonnement__salles=salle).first()
        creneaux = Creneau.range.get_creneaux_of_day().filter(abonnements=abonnement_client)

        print('LES abonnements_actives  =====', abonnements_actives)
        print('Le abonnement_client Choisi =====', abonnement_client)
        print('LES CRENEAUX =====', creneaux)

        logger.warning('LES CRENEAUX ====={}'.format(str(creneaux)))
        logger.warning('Le TYPE DABONNEMENT CRENEAUX ====={}'.format(str(abonnement_client)))

        if not abonnement_client or not creneaux:
            return False
        cren_ref = creneaux.first()
        print('Creneau de reference', cren_ref)

        if abonnement_client.is_time_volume() and abonnement_client.is_valid():
            print('abonnement_client.is_time_volume')
            logger.warning('abonnement_client.is_time_volume and is valid')
            # with transaction.atomic():
            Presence.objects.create(abc= abonnement_client, creneau=cren_ref,  hour_entree=current_time)
            self.save()
            self.remove_duplicate()
            return True
        
        elif not abonnement_client.is_time_volume() and abonnement_client.is_valid():
            print('not abonnement_client.is_time_volume')
            if creneaux.count() > 1 :
                dur_ref_time_format = abs(datetime.strptime(str(creneaux[0].hour_start), FTM) - datetime.strptime(current_time, FTM)) #nous avons besoin d'un crenaux Reference pour le comparé au autres
                dur_ref= timedelta.total_seconds(dur_ref_time_format) 
                for cr in creneaux:
                    start = str(cr.hour_start)
                    print('heure de début', start)
                    temps = abs(datetime.strptime(start, FTM) - datetime.strptime(current_time, FTM))
                    duree_seconde = timedelta.total_seconds(temps) 
                    if dur_ref > duree_seconde:
                        dur_ref = duree_seconde
                        cren_ref = cr
            with transaction.atomic():
                Presence.objects.create(abc= abonnement_client,  creneau= cren_ref,  hour_entree=current_time)
                self.save()
                self.remove_duplicate()
                abonnement_client.presence_quantity -= 1
                abonnement_client.save()
                return True
        else:
            print('WHATS THE CASE')
            logger.warning('WHATS THE CASE-- {}'.format(str(abonnement_client.type_abonnement)))
            return False

# def manual_presence(self, abc, hour_entree, hour_sortie, date, note=None):
#         logger.warning('Client requested Door Auth ===> {}'.format(str(self.id)))

#         FTM = '%H:%M:%S'
#         erreur = {"level": "error", "message": "Ce client n'a pas accés maintenant"}
#         sortie = {"level": "success", "message": f"la sortie de {self.id} a été éffectué Avec Succée"}
#         entree = {"level": "success", "message": f"Accés autoriser pour {self.id}"}
#         current_time = datetime.now().strftime("%H:%M:%S")
#         client = self
#         #client.has_permission()
#         creneaux = Creneau.range.get_creneaux_of_day().filter(abonnements__client=client).distinct()
#         # print('Les creneaux of client=====>',Creneau.objects.filter(abonnements__client=client))
#         print('creneaux du Today client=====>', creneaux)
#         logger.warning('LOGLes creneaux du Today client=====-{}'.format(str(creneaux)))
#         if len(creneaux) :
#             dur_ref_time_format = abs(datetime.strptime(str(creneaux[0].hour_start), FTM) - datetime.strptime(current_time, FTM))
#             dur_ref= timedelta.total_seconds(dur_ref_time_format) 
#             cren_ref = creneaux[0]
#             for cr in creneaux:
#                 start = str(cr.hour_start)
#                 print('heure de début', start)
#                 temps = abs(datetime.strptime(start, FTM) - datetime.strptime(current_time, FTM))
#                 duree_seconde = timedelta.total_seconds(temps) 
#                 if dur_ref > duree_seconde:
#                     dur_ref = duree_seconde
#                     cren_ref = cr
#         presence_sortie= self.init_output()
#         if presence_sortie:
#             print('YESS SORTIEEE')
#             return sortie
#         # client.has_permission()


        
        
        
    # def dettes(self):
    #     try:
    #         # dettes = AbonnementClient.objects.filter(client =self.id).aggregate(Sum('reste'))
    #         dettes = self.abonnement_client.all().aggregate(Sum('reste'))
    #     except:
    #         dettes = 0
    #     return dettes['reste__sum']


class Coach(models.Model):
    last_name       = models.CharField(max_length=50, verbose_name='Nom')
    first_name      = models.CharField(max_length=50, verbose_name='Prénom')
    civility        = models.CharField(choices=CIVILITY_CHOICES , max_length=3, default='MME', verbose_name='Civilité')
    adress          = models.CharField(max_length=200, verbose_name='Adresse', blank=True, null=True)
    phone           = models.CharField(max_length=22, verbose_name='Téléphone', blank=True, null=True)
    email           = models.CharField(max_length=50, verbose_name='E-mail',blank=True, null=True)
    nationality     = models.CharField(max_length=50, verbose_name='Nationalité')
    birth_date      = models.DateField(max_length=50, verbose_name='Date de naissance')
    blood           = models.CharField(choices=BLOOD_CHOICES , max_length=3, verbose_name='Groupe sanguin')
    date_added      = models.DateTimeField(auto_now_add=True, verbose_name='Date d\'inscription')
    state           = models.CharField(choices=STATE_CHOICES , max_length=3, verbose_name='Etat', default='A')
    note            = models.TextField(blank=True, null=True)
    salaire         = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True,default=0)
    color           = models.CharField( max_length=50, default='#333333',blank=True, null=True) 
    history = HistoricalRecords()
    # s           = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    # creneau         = models.ForeignKey(Creneau, verbose_name="créneau" , on_delete=models.CASCADE)

    # salle_activity  = models.ManyToManyField("Salle", verbose_name="salle d'activité")
    # salle_sport     = models.ManyToManyField("Salle", verbose_name="salle de sport")
    # maladies        = models.ManyToManyField(Maladie)
    heures_done     = models.IntegerField( blank=True, null=True)
    pay_per_hour    = models.IntegerField( blank=True, null=True, default=1,verbose_name='Salaire par heure')
    created      = models.DateTimeField(verbose_name='Date de Création',  auto_now_add=True)

    updated      = models.DateTimeField(verbose_name='Date de dernière mise à jour',  auto_now=True)
    objects = models.Manager()
    custom_manager = PresenceManager()

    
    def __str__(self):
        return self.last_name
    

    def get_salaire(self):
        return self.heures_done * self.pay_per_hour

    def get_view_url(self):
        return reverse("client:CoachDetail", kwargs={"pk": self.pk})
    
    def get_edit_url(self):
        return reverse('client:coach_update', kwargs={'pk': str(self.id)})

    def get_delete_url(self):
        return reverse('client:coach_delete', kwargs={'pk': str(self.id)})


    def enter_sotrie_coach(self):
        pending_presence = PresenceCoach.objects.filter(coach=self, hour_sortie__isnull=True)
        print("in_salle ------------------------", pending_presence)
        
        if not pending_presence:
            pending_presence = PresenceCoach.objects.get_or_create(
                coach=self,
                hour_entree=timezone.now().time()
            )
        else:
            pending_presence = pending_presence.first()
            pending_presence.hour_sortie = timezone.now().time()
        
            pending_presence.save()   
            
        context = {'pending_presence': pending_presence}
        print("context*******************", context)
        # print('hour_sortie --------------', pending_presence.hour_sortie)
        return self
    
    # def enter(self):
    #     pending_presence = self.get_pending_presence()
    #     print("in_salle ------------------------", pending_presence)
        
    #     if  pending_presence:
    #         pending_presence = PresenceCoach.objects.get_or_create(
    #             coach=self,
    #             hour_entree=timezone.now().time()
    #         )
    #     else:
    #         pending_presence.hour_sortie = timezone.now().time()
        
    #     context = {'pending_presence': pending_presence}
    #     print("context*******************", context)
    #     # print('hour_sortie --------------', pending_presence.hour_sortie)
    #     return self

    # def sortie(self):
    #     pending_presence = self.get_pending_presence()
    #     print("in_salle ------------------------", pending_presence)
    #     if  pending_presence:
    #         pending_presence = pending_presence.first()
    #         pending_presence.hour_sortie = timezone.now().time()
    #         pending_presence.save()  

    #     context = {'pending_presence': pending_presence}
    #     print("context*******************", context)
    #     # print('hour_sortie --------------', pending_presence.hour_sortie)
    #     return self 

    def get_pending_presence(self):
        return PresenceCoach.objects.filter(coach=self, hour_sortie__isnull=True)
        







class Personnel(models.Model):
    last_name       = models.CharField(max_length=50, verbose_name='Nom')
    first_name      = models.CharField(max_length=50, verbose_name='Prénom')
    civility        = models.CharField(choices=CIVILITY_CHOICES , max_length=3, default='MME', verbose_name='Civilité')
    adress          = models.CharField(max_length=200, verbose_name='Adresse', blank=True, null=True)
    function        = models.CharField(max_length=200, verbose_name='Fonction', blank=True, null=True)
    phone           = models.CharField(max_length=22, verbose_name='Téléphone', blank=True, null=True)
    email           = models.CharField(max_length=50, verbose_name='E-mail',blank=True, null=True)
    nationality     = models.CharField(max_length=50, verbose_name='Nationalité')
    birth_date      = models.DateField(max_length=50, verbose_name='Date de naissance')
    blood           = models.CharField(choices=BLOOD_CHOICES , max_length=3, verbose_name='Groupe sanguin')
    date_added      = models.DateTimeField(auto_now_add=True, verbose_name='Date de recrutement')
    created         = models.DateTimeField(verbose_name='Date de Création',  auto_now_add=True)
    updated         = models.DateTimeField(verbose_name='Date de dernière mise à jour',  auto_now=True)

    history         = HistoricalRecords()
    state           = models.CharField(choices=STATE_CHOICES , max_length=3, verbose_name='Etat', default='A')
    note            = models.TextField(blank=True, null=True)
    social_security = models.CharField(max_length=150)


    def __str__(self):
        return self.first_name
    

    def get_view_url(self):
        return reverse("client:personnel_detail", kwargs={"pk": self.pk})
    
    def get_edit_url(self):
        return reverse('client:personnel_update', kwargs={'pk': str(self.id)})

    def get_delete_url(self):
        return reverse('client:personnel_delete', kwargs={'pk': str(self.id)})




# @receiver(post_save, sender=Client)
# def create_client(sender, instance, created,**kwargs):
#     if created:
#         old_carte = instance.carte
#         print('old_carte', old_carte) 
#         carte = int(instance.carte)
#         print('carte', carte) 
#         instance.carte = hex(carte).upper()
#         print('LAST carte', instance.carte) 

# post_save.connect(create_client, sender=Client)