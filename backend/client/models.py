
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
from datetime import datetime, timedelta


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
    # def get_last_presence(self, client_id):
    #     client = Client.objects.get(id=client_id)
    #     try :
    #         # presence = client.presences.filter(is_in_salle=True).last().id
    #         presence = Presence.objects.filter(abc__client=client_id, is_in_salle=True).last().id
    #         # print(presence, ' JJJJJJJJJJJJJJJJJJJJJJ')
    #         return presence
    #     except:
    #         presence = False
    #         return presence
        # presence = client.presences.last().id
        # print( 'le ID de la derniere presences du', client, 'est le:', presence )

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
    created      = models.DateTimeField(verbose_name='Date de Création',  auto_now_add=True)
    profession  = models.CharField(max_length=50, blank=True, null=True)
    updated      = models.DateTimeField(verbose_name='Date de dernière mise à jour',  auto_now=True)
    # date_added  = models.DateTimeField(auto_now_add=True, verbose_name='Date d\'inscription')
    # state       = models.CharField(choices=STATE_CHOICES , max_length=3, verbose_name='Etat', blank=True, null=True)
    note        = models.TextField(blank=True, null=True)
    dette       = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True,default=0)
    dette_assurance      = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True,default=0)
    fin_assurance       = models.DateField(max_length=50, null=True, blank=True)
    maladies    = models.ManyToManyField(Maladie)
    objects     = models.Manager()
    abonnement_manager = AbonnementManager()
    history = HistoricalRecords()



    def __str__(self):
        return str(self.id)
    
    def full_name(self):
        return str(self.last_name)+ " " +str(self.first_name)

    def get_absolute_url(self):
        return reverse("client:client-detail", args={"slug": self.slug})
    
    def is_on_salle(self):
        # presences = Client.objects.prefetch_related('abonnement_client__presences', is_in_salle=True).filter(id=self.pk)
        # presences = Client.objects.filter(abonnement_client__presences_abc__is_in_salle=True, id=self.pk ).distinct()
        if True:
        # if presences:
            return True
        else: 
            print('not inb salle presences ---------------------->', presences)
            return False
    def has_permission(self, door_ip):
        FTM = '%H:%M:%S'
        current_time = datetime.now().strftime("%H:%M:%S")
        creneaux = Creneau.range.get_creneaux_of_day().filter(abonnements__client=self, activity__salle__door__ip_adress= door_ip)
        print('les creneau permis', creneaux)
        if self.is_on_salle :
            return True
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
            abon_list = AbonnementClient.objects.filter(client = self,creneaux = cren_ref, archiver = False )
            for ab in abon_list: # si il y'a plusieurs abonnement on previlegie les abonnement normal vu qu'il ne sont pas recuperable
                # print("abonnement dans la bouvcle", ab.type_abonnement.free_sessions)
                if not ab.type_abonnement.free_sessions:
                    # if AbonnementClient.validity.is_valid(ab.id):
                    abonnement = ab
                else:
                    print('je suis laaaa')
                    abonnement = ab
            # abonnement = abon_list.first()
            print('l \'abonnement du client est le :>>>>>>>>>>', abonnement)
            # is_valid = AbonnementClient.validity.is_valid(abonnement.id)
            if abonnement.is_time_volume() and abonnement.presence_quantity > 30:
                presence = Presence.objects.create(abc= abonnement, creneau= cren_ref, is_in_list=True, hour_entree=current_time, is_in_salle=True)
                return presence

            if abonnement.presence_quantity > -2:
            # AbonnementClient.validity.is_valid(obj.id)
                presence = Presence.objects.create(abc= abonnement, creneau= cren_ref, is_in_list=True, hour_entree=current_time, is_in_salle=True)
                if abonnement.is_fixed_sessions() or abonnement.is_free_sessions():
                    abonnement.presence_quantity -= 1
                abonnement.save()
                return presence
            return True
        return False

    def save(self, *args, **kwargs):
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
    # SALAIRE ======> stock all transaction to know when the personnel took money
    
    # avance          = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    # assurance   = models.ForeignKey("app.Model", verbose_name=_(""), on_delete=models.CASCADE)
    # salle_sport = models.ForeignKey("app.Model", verbose_name=_(""), on_delete=models.CASCADE)
    # abonnement  = models.ForeignKey("app.Model", verbose_name=_(""), on_delete=models.CASCADE)
    # paiement    = models.ForeignKey("app.Model", verbose_name=_(""), on_delete=models.CASCADE)
    # planning    = models.ForeignKey("app.Model", verbose_name=_(""), on_delete=models.CASCADE)
    # maladies    = models.ForeignKey("app.Model", verbose_name=_(""), on_delete=models.CASCADE)

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