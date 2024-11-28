from django.db import models
from django.urls import reverse
from django.urls import reverse
from planning.models import Planning
# from client.models import Coach
from salle_activite.models import Activity
# Create your models here.
from simple_history.models import HistoricalRecords
from datetime import datetime, time, timedelta


DAYS_CHOICES = (
    ('SA', 'Samedi'),
    ('DI', 'Dimanche'),
    ('LU', 'Lundi'),
    ('MA', 'Mardi'),
    ('ME', 'Mercredi'),
    ('JE', 'Jeudi'),
    ('VE', 'Vendredi'),
)



class RangeManager(models.Manager):
    now = datetime.now().time()
    def get_creneaux_of_day(self):
        if datetime.today().weekday() == 0:
            creneaux =Creneau.objects.filter(day='LU')
            # print('les creneaux du lundi sont !:;====>', creneaux)
            return creneaux
        elif datetime.today().weekday() == 1:
            creneaux =Creneau.objects.filter(day='MA')
            # print('les creneaux du Mardi sont !:;====>', creneaux)
            return creneaux
        elif datetime.today().weekday() == 2:
            creneaux =Creneau.objects.filter(day='ME')
            # print('les creneaux du MERCREDI sont !:;====>', creneaux)
            return creneaux
        elif datetime.today().weekday() == 3:
            creneaux =Creneau.objects.filter(day='JE')
            # print('les creneaux du JEUDI sont !:;====>', creneaux)
            return creneaux
        elif datetime.today().weekday() == 4:
            creneaux =Creneau.objects.filter(day='VE')
            # print('les creneaux du VENDREDI sont !:;====>', creneaux)
            return creneaux
        elif datetime.today().weekday() == 5:
            creneaux =Creneau.objects.filter(day='SA')
            # print('les creneaux du lundi sont !:;====>', creneaux)
            return creneaux
        elif datetime.today().weekday() == 6:
            creneaux =Creneau.objects.filter(day='DI')
            # print('les creneaux du lundi sont !:;====>', creneaux)
            return creneaux

    # def get_creneaux_of_similar_day(self, creneau_id):
    #     actual_creneau = Creneau.objects.get(id= creneau_id)
    #     creneau_day = actual_creneau.day
    #     creneaux = Creneau.objects.filter(day=creneau_day)
    #     return creneaux


    def get_creneau(self):
        new_creneaux = []
        creneaux_shifted = []
        now = datetime.now().time()
        creneaux = self.get_creneaux_of_day()
        for i in creneaux:
            # print('the i', i)
            try:
                start_hour_1 = i.hour_start.replace(hour =i.hour_start.hour, minute= i.hour_start.minute - 20)
            except:
                try:
                    start_hour_1 = i.hour_start.replace(hour =i.hour_start.hour - 1, minute= 60 + i.hour_start.minute - 20)
                except:
                    start_hour_1 = i.hour_start.replace(hour =23, minute=  60 + i.hour_start.minute - 20)
            try:
                start_hour_2 = i.hour_start.replace(hour=i.hour_start.hour, minute=i.hour_start.minute + 20)
            except:
                try:
                    start_hour_2 = i.hour_start.replace(hour=i.hour_start.hour+1, minute=i.hour_start.minute + 20 - 60)
                except:
                    start_hour_2 = i.hour_start.replace(hour=0, minute=i.hour_start.minute + 20 - 60)
            creneaux_shifted.append((start_hour_1, start_hour_2))
        for h in creneaux_shifted:
            if now >= h[0] and now <= h[1]:
                res2 = creneaux_shifted.index(h)
                creneau = creneaux[res2]
                new_creneaux.append(creneau)
        return new_creneaux
                
    def get_abc(self, abc_id):
        creneaux = self.get_creneau()

        for cr in creneaux:
            abonnements = cr.abonnements.all()
            for i in abonnements:
                # print('les IDS des abonnements liers a ce creneau', i.id)
                if i.id == abc_id:
                    return True
                else: 
                    print('jes uis laaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', abc_id, i.id)


    def get_similar_creneaux(self, creneau_id):
        actual_creneau = Creneau.objects.get(id= creneau_id)
        creneau_day = actual_creneau.day
        # print('crerenaudu jour', creneau_day)
        st_hour = actual_creneau.hour_start


        # print('heure de depart =>', st_hour)
        try:
            start_hour_1 = st_hour.replace(hour =st_hour.hour, minute= st_hour.minute - 20)
        except:
            try:
                start_hour_1 = st_hour.replace(hour =st_hour.hour - 1, minute= 60 + st_hour.minute - 20)
            except:
                start_hour_1 = st_hour.replace(hour = 23, minute=  60 + st_hour.minute - 20)
        try:
            start_hour_2 = st_hour.replace(hour=st_hour.hour, minute=st_hour.minute + 20)
        except:
            try:
                start_hour_2 = st_hour.replace(hour=st_hour.hour+1, minute=st_hour.minute + 20 - 60)
            except:
                start_hour_2 = st_hour.replace(hour=0, minute=st_hour.minute + 20 - 60)
        tous_creneaux = Creneau.objects.filter(hour_start__range=[start_hour_1,start_hour_2])
        creneaux = tous_creneaux.filter(day=creneau_day)
        return creneaux

    # def creneau_by_day(self, acti_id):
    #     cren = Creneau.objects.filter(activity=acti_id, hour_start__range=['08:00', '11:00'])
    #     return cren





class Creneau(models.Model):
    hour_start  = models.TimeField()
    hour_finish = models.TimeField()
    day         = models.CharField(choices=DAYS_CHOICES , max_length=2, default='DI', verbose_name='Jour')
    name        = models.CharField(verbose_name="nom du creneau", max_length=100,blank=True, null=True)
    planning    = models.ForeignKey(Planning, on_delete=models.CASCADE)
    color       = models.CharField( max_length=50, blank=True, null=True) 
    activity    = models.ForeignKey(Activity, verbose_name="activities", related_name="creneaux", on_delete=models.CASCADE)
    coach       = models.ForeignKey('client.Coach' , on_delete=models.CASCADE, related_name='creneaux', blank=True, null=True)
    created     = models.DateTimeField(verbose_name='Date de Création', auto_now_add=True)
    updated     = models.DateTimeField(verbose_name='Date de dernière mise à jour', auto_now=True)
    objects     = models.Manager()
    range       = RangeManager()
    history     = HistoricalRecords()
    hour_start  = models.TimeField()
    hour_finish = models.TimeField()
    day         = models.CharField(choices=DAYS_CHOICES , max_length=2, default='DI', verbose_name='Jour')
    name        = models.CharField(verbose_name="nom du creneau", max_length=100,blank=True, null=True)
    planning    = models.ForeignKey(Planning, on_delete=models.CASCADE)
    color       = models.CharField( max_length=50, blank=True, null=True) 
    activity    = models.ForeignKey(Activity, verbose_name="activities", related_name="creneaux", on_delete=models.CASCADE)
    coach       = models.ForeignKey('client.Coach' , on_delete=models.CASCADE, related_name='creneaux', blank=True, null=True)
    created     = models.DateTimeField(verbose_name='Date de Création', auto_now_add=True)
    updated     = models.DateTimeField(verbose_name='Date de dernière mise à jour', auto_now=True)
    objects     = models.Manager()
    range       = RangeManager()
    history     = HistoricalRecords()

    class Meta:
        ordering = ['hour_start']

    def __str__(self):
        return str(self.hour_start)

    def get_color(self):
        if self.color:
            print('je suis la =>', self.color)
            return self.color
        elif self.coach:
            print('je suis self.coach.color =>', self.coach.color)
            return self.coach.color
        elif self.activity.color:
            return self.activity.color
        else:
            return str("#000") 
    def get_delete_url(self):
        return reverse('creneau:creneau_delete_view', kwargs={'pk': str(self.id)})



class Event(models.Model):
    title = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
   

    def __str__(self):
        return self.title
    def get_delete_url(self):
        return reverse('creneau:creneau_delete_view', kwargs={'pk': str(self.id)})



class Event(models.Model):
    title = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
   

    def __str__(self):
        return self.title
