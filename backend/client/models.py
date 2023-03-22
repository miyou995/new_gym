
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


from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile

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
    name = models.CharField(max_length=150)
    # client = models.ForeignKey(Client, related_name="maladies", on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Maladie'
        verbose_name_plural = 'Maladies'

class Client(models.Model):
    id          = models.CharField(max_length=50, primary_key=True)
    carte       = models.CharField(max_length=100, unique=True, blank=True, null=True)
    hex_card    = models.CharField(max_length=100, unique=True, blank=True, null=True)
    last_name   = models.CharField(max_length=50, verbose_name='Nom')
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
    maladies    = models.ManyToManyField(Maladie)
    # date_added  = models.DateTimeField(auto_now_add=True, verbose_name='Date d\'inscription')
    # state       = models.CharField(choices=STATE_CHOICES , max_length=3, verbose_name='Etat', blank=True, null=True)
    dette_assurance      = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True,default=0)
    fin_assurance       = models.DateField(max_length=50, null=True, blank=True)
    objects     = models.Manager()
    abonnement_manager = AbonnementManager()
    history = HistoricalRecords()

    def __init__(self, *args, **kwargs):
        super(Client, self).__init__(*args, **kwargs)
        self._old_picture = self.picture

    def __str__(self):
        return str(self.id)

    def generate_thumbnail(self, picture, picture_name):
        THUMBNAIL_SIZE = (250, 360)
        image = Image.open(picture)
        image = image.convert("RGB")
        image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)
        temp_thumb = BytesIO()
        image.save(temp_thumb, "JPEG")
        temp_thumb.seek(0)
        # set save=False, otherwise it will run in an infinite loop
        self.picture.save(self.picture.name,ContentFile(temp_thumb.read()),save=False)
        print('DONE')
        temp_thumb.close()

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
    
    
    def save(self, *args, **kwargs):
        if self._old_picture != self.picture:
            # self.generate_thumbnail(self.picture, self.picture.name)
            print('yess changed picturename', self.picture.name)
            print('yess changed picture url', self.picture.url)
            register_user.delay(self.last_name, self.id, self.picture.name)
        else:
            print('picture not changed')
        if not self.id:
            try :
                # print('clientsd==> ', timezone.now())
                last_id = Client.objects.latest('created').id
                print('yesssss last id = ', last_id)
                number = int(last_id[1::])+1
                print('the number', number)     
                result  = str(number).zfill(4)
                print('the result', result)     
                the_id = f'C{result}'   
                print('the id', the_id)     
                self.id = the_id
            except:
                self.id = "C0001"

        if self.carte:
            # old_carte = self.carte
            # print('old_carte', old_carte) 
            int_carte = int(self.carte)
            str_carte = str(int_carte)
            print('carte', str_carte) 
            new_int_carte =  int(str_carte)
            hex_card = hex(new_int_carte)
            deleted_x = hex_card.replace('0x', '')
            self.hex_card = deleted_x.upper().zfill(8)
            print('deleted_x', deleted_x) 
            print(' hex_card', self.hex_card) 
        return super().save(*args, **kwargs)
    
    def full_name(self):
        return str(self.last_name)+ " " +str(self.first_name)

    def get_absolute_url(self):
        return reverse("client:client-detail", args={"slug": self.slug})

    #A VERIF


    def init_output(self,  exit_hour=None):
        my_presences = Presence.objects.filter(abc__client=self, is_in_salle=True)
        presence = my_presences.first()




        print('LA my_presences', my_presences)
        print('LA PRESENCE', presence)
        current_time = datetime.now().strftime("%H:%M:%S")
        if exit_hour:
            current_time = exit_hour
        if not presence:
            """ ecart + de 10 seconde"""
            return False
        presence_time = presence.hour_entree
        
        ecart = abs(datetime.strptime(current_time, FTM) - datetime.strptime(str(presence_time), FTM))
        print('ECART', ecart)
        print('ECART TYPE', type(ecart))

        time_diff_seconds = timedelta.total_seconds(ecart)
        print('time_diff_seconds================>', time_diff_seconds)
        if not time_diff_seconds > 10:
            return False
        
        presence.hour_sortie = current_time
        presence.is_in_salle = False
        presence.save()

        # update abc
        # presence.save(commit=False)
        abc = presence.abc
        if abc.is_time_volume():
            ecart = presence.get_time_consumed() 
            abc.presence_quantity -= ecart 
            abc.save()
            # ecart = abs(datetime.strptime(str(hour_start), FTM) - datetime.strptime(current_time, FTM))
        # else:
        #     abc.presence_quantity -= 1
        print('la sorite--------------- ', presence.hour_sortie)
        print('la presence.is_in_salle--------------- ', presence.is_in_salle)
        return True

    def get_access_permission(self, door_ip=None):
        my_presences = Presence.objects.filter(abc__client=self, hour_sortie__isnull=True)
        in_salle_presences = Presence.objects.filter(abc__client=self, is_in_salle=True)
        print('MY presence with hour sortie null=>', my_presences)
        print('MY presence with is is salle=>', in_salle_presences)

        current_time = datetime.now().strftime("%H:%M:%S")
        # the problem is that it doesn't turn the client is_on_salle to True on entering we can try to make comparison here if it less than 10 s we directly return False
        if self.is_on_salle or my_presences :
            print('is on salle')
            sortie = self.init_output()
            if not sortie: # if sortie is false this mean that the client passed the card on an interval < 10 secondes
                print('WAIT 10 SECONDES')  
                return False
            self.is_on_salle = False 
            self.save()
            return sortie
        door = Door.objects.filter(ip_adress=door_ip).first()
        salle = door.salle
        # salle = Salle.objects.filter(door__ip_adress=door_ip).first()
        print('Adress IP', door_ip)
        print('SAlle ', salle)
        abonnements_actives = AbonnementClient.subscription.active_subscription()
        abonnement_client = abonnements_actives.filter(client=self, type_abonnement__salles=salle).first()
        creneaux = Creneau.range.get_creneaux_of_day().filter(abonnements=abonnement_client)
        print('LES CRENEAUX =====', creneaux)
        if not abonnement_client or not creneaux:
            return False
        print('Le TYPE DABONNEMENT CRENEAUX =====', abonnement_client)

        cren_ref = creneaux.first()
        print('Creneau de reference', cren_ref)
        if abonnement_client.is_time_volume() and abonnement_client.is_valid():
            print('abonnement_client.is_time_volume')
            with transaction.atomic():
                Presence.objects.create(abc= abonnement_client, creneau=cren_ref, is_in_list=True, hour_entree=current_time, is_in_salle=True)
                self.is_on_salle=True
                self.save()
                return True
        elif not abonnement_client.is_time_volume() and abonnement_client.is_valid():
            print('not abonnement_client.is_time_volum')
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
                Presence.objects.create(abc= abonnement_client,  creneau= cren_ref, is_in_list=True, hour_entree=current_time, is_in_salle=True)
                self.is_on_salle=True
                abonnement_client.presence_quantity -= 1
                abonnement_client.save()
                self.save()
                return True
        else:
            print('WHATS THE CASE')
            return False


    def dettes(self):
        try:
            # dettes = AbonnementClient.objects.filter(client =self.id).aggregate(Sum('reste'))
            dettes = self.abonnement_client.all().aggregate(Sum('reste'))
        except:
            dettes = 0
        return dettes['reste__sum']


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
    pay_per_hour    = models.IntegerField( blank=True, null=True, default=1)
    created      = models.DateTimeField(verbose_name='Date de Création',  auto_now_add=True)

    updated      = models.DateTimeField(verbose_name='Date de dernière mise à jour',  auto_now=True)
    objects = models.Manager()
    custom_manager = PresenceManager()
    def __str__(self):
        return self.last_name

    def get_salaire(self):
        return self.heures_done * self.pay_per_hour

    def get_absolute_url(self):
        return reverse("client:coach_detail", kwargs={"pk": self.pk})




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
    created      = models.DateTimeField(verbose_name='Date de Création',  auto_now_add=True)
    updated      = models.DateTimeField(verbose_name='Date de dernière mise à jour',  auto_now=True)

    history = HistoricalRecords()
    state           = models.CharField(choices=STATE_CHOICES , max_length=3, verbose_name='Etat', default='A')
    note            = models.TextField(blank=True, null=True)
    social_security = models.CharField(max_length=150)


    def __str__(self):
        return self.first_name
    def get_absolute_url(self):
        return reverse("client:personnel_detail", kwargs={"pk": self.pk})


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