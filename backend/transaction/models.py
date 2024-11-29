from django.db import models
from abonnement.models import Abonnement, AbonnementClient
from client.models import Personnel, Coach, Client
from assurance.models import Assurance
from datetime import date, datetime
from django.urls import reverse
# Create your models here.
from django.db.models.signals import post_save, post_delete
import calendar
from simple_history.models import HistoricalRecords

class Transaction(models.Model):
    amount          = models.DecimalField(max_digits=11, decimal_places=0, default = 0)
    date_creation   = models.DateField(default=date.today)
    notes           = models.TextField(blank=True, null=True)
    last_modified   = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.amount)
    class Meta:
        ordering = ['-last_modified']
        permissions = [
            ('can_view_history', 'Can View history'),
            ('can_view_statistique', 'Can View Statistique'),
            ]

class Paiement(Transaction):
    # type = models.ForeignKey(Abonnement, verbose_name="abonnement" , related_name="abonnements", on_delete=models.CASCADE)
    abonnement_client = models.ForeignKey(AbonnementClient,on_delete=models.PROTECT, related_name='transactions')
    history = HistoricalRecords()
    # hello = models.TextField(blank=True, null=True)
    def __str__(self):
        return str(self.amount)
    class Meta:
        ordering = ['-last_modified']

    def get_abonnement_name(self):
        try:
            return self.abonnement_client.type_abonnement
        except:
            return ""

    def get_client_last_name(self):
        try:
            return self.abonnement_client.client.last_name
        except:
            return ""
    def get_client_id(self):
        try:
            return self.abonnement_client.client.id
        except:
            return ""
    @property
    def get_abc_price(self):
        return self.abonnement_client.type_abonnement.price
    
    @property
    def get_abc_reste(self):
        return self.abonnement_client.reste
    

    
    def get_url(self,pk):
        return reverse('client:client_detail', kwargs={'pk':pk})
    def get_edit_url(self):
        return reverse('transactions:paiement_update', kwargs={'pk': str(self.id)})

    def get_delete_url(self):
        return reverse('transactions:PaiementDeleteView_name', kwargs={'pk': str(self.id)})

    @classmethod
    def get_total_by_subscription_type(cls):
        from django.db.models import Sum
        return (cls.objects
                .values('abonnement_client__type_abonnement__name')
                .annotate(total=Sum('amount'))
                .order_by('abonnement_client__type_abonnement__name'))
class Autre(Transaction):
    history = HistoricalRecords()
    name = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return str(self.amount)
    class Meta:
        ordering = ['-date_creation']

    def get_url(self):
        return reverse('client:client_detail', kwargs={'pk':str(self.id)})
    def get_edit_url(self):
        return reverse('transactions:autre_transaction_update', kwargs={'pk': str(self.id)})

    def get_delete_url(self):
        return reverse('transactions:autre_transaction_delete', kwargs={'pk': str(self.id)})  

class AssuranceTransaction(Transaction):
    # type = models.CharField(max_length=200, null=True, blank=True)
    history = HistoricalRecords()
    client = models.ForeignKey(Client,on_delete=models.SET_NULL, related_name='assurances',blank=True, null=True)

    def __str__(self):
        return str(self.amount)

    class Meta:
        ordering = ['-date_creation']

    


class Remuneration(Transaction):
    history = HistoricalRecords()
    nom = models.ForeignKey(Personnel, related_name="rem_personnels", on_delete=models.SET_NULL,blank=True, null=True)
    def __str__(self):
        return str(self.amount)
    class Meta:
        ordering = ['-date_creation']

    def get_url(self,pk):
        return reverse('client:personnel_detail', kwargs={'pk':pk})
    def get_edit_url(self):
        return reverse('transactions:Remuneration_Personnel_update', kwargs={'pk': str(self.id)})
    def get_delete_url(self):
        return reverse('transactions:RemuPersonnelDeleteView_name', kwargs={'pk': str(self.id)})
    
        
class RemunerationProf(Transaction):
    history = HistoricalRecords()
    coach = models.ForeignKey(Coach, related_name="rem_coachs", on_delete=models.SET_NULL,blank=True, null=True)
    def __str__(self):
        return str(self.amount)
    class Meta:
        ordering = ['-date_creation']

    def get_url(self,pk):
        return reverse('client:CoachDetail', kwargs={'pk':pk})
    def get_edit_url(self):
        return reverse('transactions:Remuneration_Coach_update', kwargs={'pk': str(self.id)})
    def get_delete_url(self):
        return reverse('transactions:RemCoachDeleteView_name', kwargs={'pk': str(self.id)})





def paiement_signal(sender, instance, **kwargs):
    id_client = instance.abonnement_client.client.id
    id_abc = instance.abonnement_client.id
    client = Client.objects.get(id=id_client)
    abc = AbonnementClient.objects.get(id=id_abc)
    price = instance.amount
    # print('les paiements', abc.transactions.all())
    try:
        client.dette -= price
        abc.reste -= price
    except:
        client.dette = price
        abc.reste = 0
    client.save()
    abc.save()

def paiement_delete_signal(sender, instance, **kwargs):
    id_client = instance.abonnement_client.client.id
    id_abc = instance.abonnement_client.id
    client = Client.objects.get(id=id_client)
    abc = AbonnementClient.objects.get(id=id_abc)
    price = instance.amount
    client.dette += price
    abc.reste += price
    client.save()
    abc.save()


post_save.connect(paiement_signal, sender=Paiement)
post_delete.connect(paiement_delete_signal, sender=Paiement)
# post_save.connect(paiement_assurance_signal, sender=AssuranceTransaction)

def salaire_coach_signal(sender, instance, created, **kwargs):
    if created:
        id_coach = instance.coach.id
        coach = Coach.objects.get(id=id_coach)
        montant = instance.amount
        coach.salaire -= montant
        coach.save()

post_save.connect(salaire_coach_signal, sender=RemunerationProf)

def fin_assurance_signal(sender, instance, created, **kwargs):
    if created:
        try:
            id_client = instance.client.id
            client = Client.objects.get(id=id_client)
            this_year = datetime.now().year
            this_month = datetime.now().month
            this_day = datetime.now().day

            if this_month == 1:
                fin_year = this_year
                fin_month = 12
                fin_day = calendar.monthrange(fin_year, fin_month)[1]
                
            else: 
                fin_year = this_year +1
                fin_month = this_month -1
                fin_day = calendar.monthrange(fin_year, fin_month)[1]
                
            date_fin = datetime(fin_year, fin_month, fin_day)
            client.fin_assurance = date_fin
            client.save()
        except:
            print('waht is this', instance.id)    
            print('waht is this', instance.__class__)    

post_save.connect(fin_assurance_signal, sender=AssuranceTransaction)
