from django.db import models
# Create your models here.

class SalleManager(models.Manager):
    def default_salle(self):
        salle = Salle.objects.last()
        if Salle.objects.filter(is_default=True).exists():
            salle = Salle.objects.filter(is_default=True).last()
        return salle



class Salle(models.Model):
    name = models.CharField(max_length=50, verbose_name="nom de la salle d'activité")
    is_default      = models.BooleanField(default=False)
    # coach = models.ManyToManyField("app.Coach")
    objects = models.Manager()
    custom_manager = SalleManager()
    class Meta:
        pass
        # unique together
    def __str__(self):
        return self.name
        
    @property
    def get_door(self):
        first_door = self.doors.first().ip_adress 
        return first_door 

    def save(self, *args, **kwargs):
        if self.is_default:
            self.is_default = True
            update_default = Salle.objects.all().exclude(id=self.id).update(is_default=False)
        super(Salle, self).save(*args, **kwargs)
        
class Door(models.Model):
    ip_adress = models.CharField(max_length=20, verbose_name="Adresse ip de la porte")
    salle      = models.ForeignKey(Salle, on_delete=models.CASCADE, related_name='doors', blank=True, null=True)
    username  = models.CharField(max_length=50, verbose_name="username de la porte")
    password  = models.CharField(max_length=30, verbose_name="password de la porte")
    def __str__(self):
        return self.ip_adress
    
    @property
    def salle_name(self):
        return self.salle.name or ''

class Activity(models.Model):
    name    = models.CharField( max_length=150, verbose_name="nom d'activité")
    salle   = models.ForeignKey(Salle, on_delete=models.CASCADE, related_name='actvities')
    color   = models.CharField( max_length=50, default="#233774",blank=True, null=True) 
    
    def __str__(self):
        return self.name











 