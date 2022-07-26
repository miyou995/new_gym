from django.db import models
from salle_activite.models import Salle
# Create your models here.

class Materiel(models.Model):
    name            = models.CharField(max_length=50, verbose_name="nom")
    quantity        = models.PositiveIntegerField()
    note            = models.CharField(max_length=50, verbose_name="remarque", blank=True, null=True)
    inscription_date= models.DateField(auto_now_add=True, verbose_name="date d'ajout")
    salle_activite  = models.ForeignKey(Salle, verbose_name="salle d'activité", on_delete=models.CASCADE, blank=True, null=True)


# class Consommable(models.Model):
