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
    created         = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)
    objects         = models.Manager()
    custom_manager  = PlanningManager()
    # activite        = models.ManyToManyField("Activity", verbose_name="Activité")
    # salle_activite  = models.ManyToManyField("Salle", verbose_name="salle d'activité")
    # prof            = models.ManyToManyField("Coach", verbose_name="Coach")
    # creneau         = models.ManyToManyField("Creneau", verbose_name="créneau")
    # client          = models.ManyToManyField("Client")
    class Meta:
        ordering= ('-created',)
    def __str__(self):
        return self.name



    def save(self, *args, **kwargs):
        if self.is_default:
            self.is_default = True
            Planning.objects.all().exclude(id=self.id).update(is_default=False)
        super(Planning, self).save(*args, **kwargs)
