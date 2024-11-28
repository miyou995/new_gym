from django.contrib import admin
from .models import  Paiement,Remuneration,RemunerationProf,Autre
# Register your models here.




@admin.register(Paiement)
class cliAdmin(admin.ModelAdmin):
    list_display = (  "abonnement_client",
                    "amount",
                    
        
       )
  

admin.site.register(Remuneration)
admin.site.register(RemunerationProf)
admin.site.register(Autre)
