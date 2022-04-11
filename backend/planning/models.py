from django.db import models
from salle_sport.models import SalleSport

class PlanningManager(models.Manager):
    def default_planning(self):
        planning = Planning.objects.last()
        if Planning.objects.filter(is_default=True).exists():
            planning = Planning.objects.filter(is_default=True).last()
        return planning

class Planning(models.Model):
    name            = models.CharField(max_length=200)
    salle_sport     = models.ForeignKey(SalleSport, verbose_name="Salle de sport", related_name='plannings', on_delete=models.CASCADE, null=True, blank=True)
    is_default      = models.BooleanField(default=True)
    objects = models.Manager()
    custom_manager = PlanningManager()
    # activite        = models.ManyToManyField("Activity", verbose_name="Activité")
    # salle_activite  = models.ManyToManyField("Salle", verbose_name="salle d'activité")
    # prof            = models.ManyToManyField("Coach", verbose_name="Coach")
    # creneau         = models.ManyToManyField("Creneau", verbose_name="créneau")
    # client          = models.ManyToManyField("Client")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Planning_detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        if self.is_default:
            self.is_default = True
            update_default = Planning.objects.all().exclude(id=self.id).update(is_default=False)
        super(Planning, self).save(*args, **kwargs)
