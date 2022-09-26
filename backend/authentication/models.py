from django.db import models
from django.contrib.auth.models import (AbstractUser, BaseUserManager)
# Create your models here.

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password,**extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields) 
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self._create_user(email, password, **extra_fields)
       
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_active") is not True:
            raise ValueError("Superuser must have is_active=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(email, password, **extra_fields)
    


class User(AbstractUser):
    username        = None
    email           = models.EmailField('email address', unique=True)
    first_name      = models.CharField(max_length=70, verbose_name="Nom", blank=True, null=True)
    last_name       = models.CharField(max_length=70, verbose_name="Prénom", blank=True, null=True)
    is_active       = models.BooleanField(default=False)
    is_manager      = models.BooleanField(default=False)
    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = []
    objects         = UserManager()
    
    @property
    def is_assistant(self):
        return self.is_active and (self.is_superuser or self.is_staff and self.groups.filter(name="Assistant").exists())
    @property
    def is_developer(self):
        return self.is_active and (self.is_superuser or self.is_staff and self.groups.filter(name="Developer").exists())
    @property
    def is_commercial(self):
        return self.is_active and (self.is_superuser or self.is_staff and self.groups.filter(name="Commercial").exists())
    @property
    def is_marketer(self):
        return self.is_active and (self.is_superuser or self.is_staff and self.groups.filter(name="Marketer").exists())
    @property
    def is_content_creator(self):
        return self.is_active and (self.is_superuser or self.is_staff and self.groups.filter(name="Content_creator").exists())
    
    @property
    def get_first_group(self):
        if self.groups.first() :
            return self.groups.first().name
