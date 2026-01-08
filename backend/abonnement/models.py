import json
from datetime import date, datetime, timedelta

from creneau.models import Creneau
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.db.models import Q

# Signals imports
from django.db.models.signals import post_save
from django.urls import reverse
from salle_activite.models import Activity, Salle


class SubscriptionQuerySet(models.QuerySet):
    def time_volume(self):
        return self.filter(type_abonnement__type_of="VH")

    def free_access(self):
        return self.filter(type_abonnement__type_of="AL")

    def fixed_sessions(self):
        return self.filter(type_abonnement__type_of="SF")

    def free_sessions(self):
        return self.filter(type_abonnement__type_of="SL")

    def free_access_subscription(self):
        return self.exclude(type_abonnement__type_of="SF")

    def active_subscription(self):
        today = date.today()
        return self.filter(end_date__gte=today)

    def valid_presences(self, limite_presence=0):
        return self.exclude(type_abonnement__type_of="VH").filter(
            seances_quantity__gte=limite_presence
        )

    def valid_time(self, hlimit=30):
        return self.filter(
            Q(type_abonnement__type_of="VH") & Q(seances_quantity__gte=hlimit)
        )


class SubscriptionManager(models.Manager):
    def get_queryset(self):
        return SubscriptionQuerySet(self.model, using=self._db)

    def time_volume(self):
        return self.get_queryset().time_volume()

    def free_access(self):
        return self.get_queryset().free_access()

    def fixed_sessions(self):
        return self.get_queryset().fixed_sessions()

    def free_sessions(self):
        return self.get_queryset().free_sessions()

    def free_access_subscription(self):
        return self.get_queryset().free_access_subscription()

    def active_subscription(self):
        return self.get_queryset().active_subscription()

    def valid_presences(self):
        return self.get_queryset().valid_presences()

    def valid_time(self):
        return self.get_queryset().valid_time()


TYPE_ABONNEMENT = (
    ("VH", "Volume Horaire"),
    ("AL", "Accés Libre"),
    ("SF", "Seances Fix"),
    ("SL", "Seances Libre"),
)
DURE_ABONNEMENT = (
    ("1", "1 Jour"),
    ("15", "15 Jours"),
    ("45", "45 Jours"),
    ("30", "1 mois"),
    ("60", "2 mois"),
    ("90", "3 mois"),
    ("120", "4 mois"),
    ("150", "5 mois"),
    ("180", "6 mois"),
)


class Abonnement(models.Model):
    name = models.CharField(max_length=70, verbose_name="Nom")
    type_of = models.CharField(
        choices=TYPE_ABONNEMENT,
        max_length=2,
        default="VH",
        verbose_name="type d'abonnement",
    )
    price = models.DecimalField(max_digits=15, decimal_places=0, verbose_name="prix")
    length = models.CharField(
        choices=DURE_ABONNEMENT, verbose_name="Durée", max_length=8
    )  # number of days
    seances_quantity = models.IntegerField(
        blank=True, null=True, verbose_name="Nombre de séances/Heures"
    )
    salles = models.ManyToManyField(Salle, related_name="abonnements")
    actif = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        permissions = [("can_view_history", "Can View history")]

    def time_volume(self):
        return True if self.type_of == "VH" else False

    def free_access(self):
        return True if self.type_of == "AL" else False

    def fixed_sessions(self):
        return True if self.type_of == "SF" else False

    def free_sessions(self):
        return self.type_of == "SL"

    def get_delete_url(self):
        return reverse("core:type_abonnement_delete_view", kwargs={"pk": str(self.id)})


class AbonnementClient(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    client = models.ForeignKey(
        "client.Client", related_name="abonnement_client", on_delete=models.PROTECT
    )
    type_abonnement = models.ForeignKey(
        Abonnement, related_name="type_abonnement_client", on_delete=models.CASCADE
    )
    presence_quantity = models.IntegerField(blank=True, null=True)
    creneaux = models.ManyToManyField(
        Creneau, verbose_name="créneau", related_name="abonnements", blank=True
    )
    reste = models.DecimalField(
        max_digits=15, decimal_places=0, verbose_name="Reste", blank=True, null=True
    )
    archiver = models.BooleanField(default=False)
    created_date_time = models.DateTimeField(auto_now_add=True)
    updated_date_time = models.DateTimeField(auto_now=True)
    # blocking_date = models.DateField(null=True, blank=True)
    # already_blocked = models.BooleanField(verbose_name=_("Déjà bloqué"), default=False)
    # Lock system
    is_locked = models.BooleanField(default=False)
    has_been_locked_once = models.BooleanField(default=False)
    lock_start_date = models.DateField(null=True, blank=True)
    lock_duration_days = models.PositiveIntegerField(null=True, blank=True)  # 10/15/30

    objects = models.Manager()
    subscription = SubscriptionManager()

    def __str__(self):
        status = "✅ payé" if self.reste == 0 else f"💰 {self.reste} DA"

        return f"📅 {self.type_abonnement} | {status} | {self.start_date}"

    def get_edit_url(self):
        return reverse(
            "abonnement:update_abonnement_client", kwargs={"pk": str(self.id)}
        )

    def get_delete_url(self):
        return reverse("abonnement:abonnemt_client_delete", kwargs={"pk": str(self.id)})

    def is_time_volume(self):
        return self.type_abonnement.type_of == "VH"

    def is_free_access(self):
        return self.type_abonnement.type_of == "AL"

    def is_fixed_sessions(self):
        return self.type_abonnement.type_of == "SF"

    def is_free_sessions(self):
        return self.type_abonnement.type_of == "SL"

    # def put_archiver(self):
    #     self.archiver = True
    #     self.actif = False
    #     self.creneaux.set([])
    #     self.save()
    #     print("ABCCCCC DELETEEDDDD")
    #     return self

    def lock(self, block_date, duration_days: int):
        if self.has_been_locked_once:
            raise ValueError("This subscription has already been locked once.")

        if self.is_locked:
            raise ValueError("Subscription is already locked.")

        # if duration_days not in [10, 15, 30]:
        #     raise ValueError("Lock duration must be 10, 15, or 30 days.")

        self.is_locked = True
        self.has_been_locked_once = True
        self.lock_start_date = datetime.strptime(block_date, "%Y-%m-%d").date()
        self.lock_duration_days = duration_days

        self.save()
        return True

    def unlock(self):
        if not self.is_locked:
            return False

        locked_days = self.lock_duration_days or 0
        self.end_date = self.end_date + timedelta(days=locked_days)

        # Reset lock fields
        self.is_locked = False
        self.lock_start_date = None
        self.lock_duration_days = None

        self.save()
        return True

    def should_auto_unlock(self):
        if not self.is_locked or not self.lock_start_date:
            return False

        unlock_date = self.lock_start_date + timedelta(days=self.lock_duration_days)
        return date.today() >= unlock_date

    def toggle_lock(self):
        if self.is_locked:
            self.unlock()
        else:
            self.lock()

    # def is_abc_locked(self):
    #     return True if self.blocking_date else False

    def get_day_index(self, day):
        if day == "DI":
            return 6
        elif day == "LU":
            return 0
        elif day == "MA":
            return 1
        elif day == "ME":
            return 2
        elif day == "JE":
            return 3
        elif day == "VE":
            return 4
        elif day == "SA":
            return 5
        else:
            return False

    def get_next_date(self, given_start_date, day):
        formated_start_date = datetime.strptime(given_start_date, "%Y-%m-%d")
        weekday = formated_start_date.weekday()
        print("TODAY DE TODAY", weekday)
        the_next_date = formated_start_date + timedelta((day - weekday) % 7)
        return the_next_date

    def get_end_date(self, start_date, creneaux):
        duree = self.type_abonnement.length
        # print('get_end_date start_date => ', start_date)
        # print('get_end_date duree => ', duree)
        duree = int(duree)
        duree_semaine = (duree // 7) - 1
        # print('get_end_date duree_semaine => ', duree_semaine)
        dates_array = []
        formated_start_date = datetime.strptime(start_date, "%Y-%m-%d")
        # print('get_end_date formated_start_date => ', formated_start_date)
        calculated_end_date = formated_start_date + timedelta(days=duree)
        # print('get_end_date calculated_end_date 1 => ', calculated_end_date)
        if self.is_fixed_sessions():
            for creneau in creneaux:
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

    def get_left_minutes(self):
        minutes = self.presence_quantity
        # time = divmod(minutes, 60)
        # print('en heures', time)
        # time_string = "{}H: {}M".format(time[0], time[1])
        # print('en time_string', time_string)
        # return time_string
        if minutes < 0:
            abs_minutes = abs(minutes)
            hours, minutes = divmod(abs_minutes, 60)
            return "-{}H: {:02d}M".format(hours, minutes)
        else:
            hours, minutes = divmod(minutes, 60)
            return "{}H: {:02d}M".format(hours, minutes)

    def is_no_more_actif(self):
        today = date.today()
        if today > self.end_date:
            return True
        else:
            return False

    def is_valid(self):
        today = date.today()
        print("self.blocking_date", self.is_locked)
        print("end_date", self.end_date)
        print("end_datoday <= self.end_datete", today <= self.end_date)
        if today <= self.end_date and not self.is_locked:
            print("makach blocking", self.is_locked)
            if self.presence_quantity > self.get_limit():
                return True
        return False

    def get_type(self):
        return self.type_abonnement.get_type_of_display()

    def get_planning(self):
        try:
            # print('creneaaaau', self.creneaux.first().planning)
            return self.creneaux.first().planning
        except:
            return None

    def get_activites(self):
        activities = Activity.objects.filter(
            salle__abonnements__type_abonnement_client=self
        )
        # activites = self.type_abonnement.salles.activities
        print("les activité de cet abc ", activities)
        print("SELF ABONNE ID", self.id)
        print("SELF type_abonnement ID", self.type_abonnement)

        # activities2 = self.type_abonnement.salles.all()
        # print('ACTI 2-----------------------------------------------', activities2)
        return activities

    def renew_abc(self, renew_start_date):
        type_abonnement = self.type_abonnement
        # delta = timedelta(days = type_abonnement.length)
        creneaux = self.creneaux.all()
        # creneaux_ids = self.creneaux.all().values_list('id', flat=True)
        new_end_date = self.get_end_date(renew_start_date, creneaux)
        print("the renew_start_date", renew_start_date)
        print("the new_end_date", new_end_date)
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

    def get_limit(self):
        if self.is_time_volume():
            limit = 30
        else:
            limit = 0
        return limit

    def get_quantity_str(self):
        if self.is_time_volume():
            minutes = self.presence_quantity
            time = divmod(minutes, 60)
            # print('en heures', time)
            time_string = "{}H: {}M".format(time[0], time[1])
            # print('en time_string', time_string)
            return time_string
        else:
            return str(self.presence_quantity) + str(" Seances")

    def is_red(self):
        if self.presence_quantity <= self.get_limit():
            return "text-danger"
        return ""

    def get_selected_events(self):
        abc = AbonnementClient.objects.filter(pk=self.pk)

        selected_events_data = list(
            abc.values(
                "creneaux__pk",
                "creneaux__name",
                "creneaux__hour_start",
                "creneaux__hour_finish",
                "type_abonnement",
                "start_date",
            )
        )

        return json.dumps(selected_events_data, cls=DjangoJSONEncoder)


class BlockAbonnementClient(models.Model):
    abonnement_client = models.ForeignKey(
        AbonnementClient,
        related_name="blocked_abonnement_client",
        on_delete=models.CASCADE,
    )
    block_date = models.DateField()
    created_date_time = models.DateTimeField(auto_now_add=True)
    updated_date_time = models.DateTimeField(auto_now=True)


from django.dispatch import receiver


@receiver(post_save, sender=Creneau)
def creneau_created_signal(sender, instance, created, **kwargs):
    if not created:
        return

    activity = instance.activity
    planning = instance.planning  # FK field, safe to get directly

    abonnements = (
        AbonnementClient.subscription.active_subscription()
        .filter(
            Q(type_abonnement__type_of__in=["VH", "AL"]),
            type_abonnement__salles__actvities=activity,
            creneaux__planning=planning,
        )
        .distinct()
        .only("id")  # tiny optimization: fetch only PKs
    )

    # Bulk assign this creneau to all abonnements (M2M bulk insert)
    instance.abonnements.add(*abonnements)


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


def abonnement_client_signal(sender, instance, created, **kwargs):
    if created:
        seances_qty = instance.type_abonnement.seances_quantity

        if instance.type_abonnement.time_volume():
            seances_qty = seances_qty * 60
        instance.presence_quantity = seances_qty

        print("signalllllllllllll-------------------", seances_qty)
        reste = instance.type_abonnement.price
        instance.reste = reste
        instance.save()
        print("signalllllllllllll from client-------------------", reste)


post_save.connect(abonnement_client_signal, sender=AbonnementClient)


# def abonnement_client_signal(sender,instance, created,**kwargs):
#     from transaction.models import Paiement

#     if created:
#         id_paiement = Paiement.objects.filter(abonnement_client__pk=instance.pk)
#         print("id_paiement----------------",id_paiement)
#         if id_paiement :
#                 instance.presence_quantity=instance.presence_quantity
#                 instance.reste = instance.reste
#                 instance.save()
#                 print("signalll payeeeeeeeeeeeeee-------------------")
#         else :
#             seances_qty = instance.type_abonnement.seances_quantity
#             instance.presence_quantity = seances_qty
#             print("signalllll-------------------",seances_qty)
#             reste = instance.type_abonnement.price
#             instance.reste =reste
#             instance.save()
#             print("signalllllllllllll from client-------------------",reste)
# post_save.connect(abonnement_client_signal, sender=AbonnementClient)
