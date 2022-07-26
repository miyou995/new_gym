from django.db import models

# Create your models here.
class Assurance(models.Model):
    price      = models.DecimalField(max_digits=9, decimal_places=0, verbose_name="prix")
    start_date = models.DateField(auto_now_add=True)
    end_date   = models.DateField()
    # paiement = models.ForeignKey("app.Model", verbose_name=_(""), on_delete=models.CASCADE)
    def __str__(self):
        return str(self.price)

#### methodf calcule end date date aujourdhui plus un an