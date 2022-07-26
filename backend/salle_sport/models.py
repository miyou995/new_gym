from django.db import models
# from client.models import Coach
# Create your models here.
class SalleSport(models.Model):
    name    = models.CharField( max_length=50)
    adresse = models.CharField( max_length=50)
    phone   = models.CharField(max_length=50)
    # coach  = models.ManyToManyField(Coach, verbose_name="salle d'activité")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("SalleSport_detail", kwargs={"pk": self.pk})
