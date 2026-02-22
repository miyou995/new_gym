# Create your models here.
from datetime import date, datetime, timedelta, timezone

from abonnement.models import AbonnementClient

# from client.models import Coach
from creneau.models import Creneau
from django.db import models
from django.urls import reverse
from django.utils import timezone

FTM = "%H:%M:%S"


class PresenceManager(models.Manager):
    def get_presence(self, client_id):
        # client = Client.objects.get(id=client_id)
        presences = Presence.objects.filter(
            abc__client__id=client_id, hour_sortie__isnull=True
        )
        print("TRUEEEEEEEEEEEE", presences)
        print("client_id", client_id)
        try:
            presence = presences.last().id
        except:
            presence = False
        print("TRUEEEEEEEEEEEE", presence)
        return presence


class Presence(models.Model):
    abc = models.ForeignKey(
        AbonnementClient,
        on_delete=models.CASCADE,
        related_name="presences",
        verbose_name="Abonnement client",
    )
    date = models.DateField(
        default=timezone.now, auto_now=False, auto_now_add=False, blank=True, null=True
    )
    creneau = models.ForeignKey(
        Creneau,
        on_delete=models.CASCADE,
        related_name="presenses",
        null=True,
        blank=True,
    )
    is_in_list = models.BooleanField(
        default=True
    )  # check if the person is in the list of client that should be in this creneau
    hour_entree = models.TimeField()
    hour_sortie = models.TimeField(auto_now_add=False, null=True, blank=True)
    is_in_salle = models.BooleanField(default=False)
    # remote_device = models.BooleanField(default=False)
    note = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(verbose_name="Date de Création", auto_now_add=True)
    updated = models.DateTimeField(
        verbose_name="Date de dernière mise à jour", auto_now=True
    )
    objects = models.Manager()
    presence_manager = PresenceManager()

    class Meta:
        ordering = ["-created"]

    def save(self, *args, **kwargs):
        # print(' Save() on Presence class ( model)')
        if not self.date:
            self.date = datetime.now().date()
        # self.full_clean()
        return super().save(*args, **kwargs)

    def get_time_consumed(self, sortie=None):
        print("=========== get_time_consumed called ===========")
        today = date.today()
        # use the given presence date or default to today
        base_date = self.date if self.date else today
        print(f"base_date: {base_date}")

        if sortie:
            print("sortie hour from model +++++++", sortie)
            if isinstance(sortie, str):
                try:
                    sortie = datetime.strptime(sortie, FTM).time()
                except ValueError:
                    sortie = datetime.now().time()
            d_end = datetime.combine(base_date, sortie)
            self.hour_sortie = sortie
        else:
            # use self.hour_sortie if it is set
            if self.hour_sortie:
                exit_hour = self.hour_sortie
                if isinstance(exit_hour, str):
                    try:
                        exit_hour = datetime.strptime(exit_hour, FTM).time()
                    except ValueError:
                        exit_hour = datetime.now().time()
            else:
                exit_hour = datetime.now().time()

            d_end = datetime.combine(base_date, exit_hour)
            self.hour_sortie = exit_hour
        print(f"d_end: {d_end}")

        if self.abc.is_time_volume():
            entry_hour = self.hour_entree
            if isinstance(entry_hour, str):
                try:
                    entry_hour = datetime.strptime(entry_hour, FTM).time()
                except ValueError:
                    # fallback to now if we can't parse it
                    entry_hour = datetime.now().time()

            d_start = datetime.combine(base_date, entry_hour)
            print(f"d_start: {d_start}")

            # Handle wraparound if duration crosses midnight
            if d_end < d_start:
                d_end += timedelta(days=1)
                print(f"Wraparound applied, new d_end: {d_end}")

            diff = d_end - d_start
            diff_secondes = diff.total_seconds()
            minutes = diff_secondes / 60
            ecart = int(minutes)
            print(f"Time consumed: {ecart} minutes")
        else:
            ecart = 1
            print("Not time volume, ecart = 1")

        return ecart

    def calculate_duration_minutes(self):
        print("=========== calculate_duration_minutes called ===========")
        if self.hour_sortie:
            # Combine date with time to calculate timedelta
            base_date = self.date if self.date else datetime.now().date()
            entree = datetime.combine(base_date, self.hour_entree)
            sortie = datetime.combine(base_date, self.hour_sortie)
            print(f"entree: {entree}, sortie: {sortie}")

            # Handle wraparound if duration crosses midnight
            if sortie < entree:
                sortie += timedelta(days=1)
                print(f"Wraparound applied, new sortie: {sortie}")

            # Calculate duration
            duration = sortie - entree
            minutes = duration.total_seconds() // 60
            print(f"Duration: {minutes} minutes")
            return minutes  # Convert seconds to minutes
        print("No hour_sortie, returning None")
        return None

    def get_edit_url(self):
        return reverse(
            "presence:presence_manuelle_update_client", kwargs={"pk": str(self.id)}
        )

    def get_delete_url(self):
        return reverse(
            "presence:Presence_manuelle_delete_client", kwargs={"pk": str(self.id)}
        )

    # def get_time_consumed(self, sortie=None):
    #     if not sortie :
    #         sortie = datetime.now().time()
    #     ecart = timedelta(sortie) - timedelta(self.hour_entree)
    #     print('ECART', ecart)
    #     return ecart


class PresenceCoach(models.Model):
    coach = models.ForeignKey(
        "client.Coach",
        on_delete=models.CASCADE,
        related_name="presencesCoach",
        null=True,
        blank=True,
    )
    date = models.DateField(auto_now_add=True)
    # creneau     = models.ForeignKey(Creneau, on_delete=models.CASCADE,related_name='presencesCoach', null=True, blank=True)
    hour_entree = models.TimeField(auto_now_add=False, null=True, blank=True)
    hour_sortie = models.TimeField(auto_now_add=False, null=True, blank=True)
    is_in_salle = models.BooleanField(default=False)  # TODO remove this


def presence_coach_create_signal(sender, instance, created, **kwargs):
    FTM = "%H:%M:%S"
    if created:
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
