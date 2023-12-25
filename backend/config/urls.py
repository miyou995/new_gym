"""acm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.views.generic import TemplateView

from django.contrib import admin
from django.urls import path, include, re_path
from config import settings
from django.conf.urls.static import static
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rest-api/', include('client.urls')),
    path('rest-api/', include('abonnement.urls')),
    path('rest-api/auth/', include('authentication.urls')),
    path('rest-api/creneau/', include('creneau.urls')),
    path('rest-api/materiel/', include('materiel.urls')),
    path('rest-api/presence/', include('presence.urls')),
    path('rest-api/salle-sport/', include('salle_sport.urls')),
    path('rest-api/transactions/', include('transaction.urls')),
    path('rest-api/planning/', include('planning.urls')),
    path('rest-api/assurance/', include('assurance.urls')),
    path('rest-api/salle-activite/', include('salle_activite.urls')),
    path('rest-api/api-auth/', include('rest_framework.urls')),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    path ('',TemplateView.as_view(template_name="index.html"), name='index'),
    re_path(r'^(?:.*)/?$', TemplateView.as_view(template_name="index.html"), name='index'),


    # path('markdownx/', include('markdownx.urls')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls)),] 
# else:
#     path ('',TemplateView.as_view(template_name="index.html"), name='index'),
#     re_path(r'^(?:.*)/?$', TemplateView.as_view(template_name="index.html"), name='index'),



    
# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# else:
#     urlpatterns += path('taksit-admin/', admin.site.urls),


