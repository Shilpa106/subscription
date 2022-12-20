from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager
from rest_framework_simplejwt.tokens import RefreshToken

# Create your models here.

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    

    def __str__(self):
        return self.email

    
    def tokens(self):
        refresh=RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }


def unique_rand():
    '''
    For generating unique_id in user profile
    '''
    while True:
        code =CustomUser.objects.make_random_password(length=8)
        if not Profile.objects.filter(unique_id=code).exists():
            return code 


class Profile(models.Model):
    GENDER=[
        ('M','Male'),
        ('F','Female'),
        ('O','Other')
    ]
    user                = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    unique_id           = models.CharField(max_length=8, default=unique_rand, unique=True, blank=True, editable=False)
    first_name          = models.CharField(max_length=50, default="", null=True, blank=True)
    last_name           = models.CharField(max_length=50, default="", null=True, blank=True)
    display_name        = models.CharField(max_length=50, default="", null=True, blank=True)
    avtar               = models.ImageField(upload_to='files/profile', null=True, blank=True)
    gender              = models.CharField(max_length=2, choices=GENDER, default="", null=True, blank=True)
    age                 = models.PositiveIntegerField(default=0, blank=True, null=True)
    date_of_birth       = models.DateField(null=True, blank=True)
    zipcode             = models.CharField(max_length=25, default="", blank=True, null=True)
    street_address      = models.CharField(max_length=256,null=True,blank=True)
    apartment           = models.CharField(max_length=256,null=True,blank=True)
    ethnicity           = models.CharField(max_length=256,null=True,blank=True)
    town                = models.CharField(max_length=256,blank=True,null=True)
    country             = models.CharField(max_length=50, blank=True, null=True, default="")
    isAccount_verified  = models.BooleanField(default=True)
    which_sociailmedia  = models.CharField(max_length=50, default="", null=True, blank=True)

    def __str__(self):
        return self.user.email

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance,created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()




class Subscription(models.Model):
    '''
    Subscription model foelds for user monthly subscription

    '''
    subscription_type = [
        ('F', 'Fre trial'),
        ('M', 'Medium'),
        ('P', 'Paid'),]
    type                = models.CharField(max_length=200, choices=subscription_type, default="", null=True, blank=True)

    title               = models.CharField(max_length=100, blank=True)
    description         = models.TextField(blank=True)
    price               = models.FloatField(blank=True)
    validity            = models.DateField()
    is_popular          = models.PositiveIntegerField(default=0)
    users_enrolled      = models.PositiveIntegerField(default=0)
    is_active           = models.BooleanField(default=True)

    def __str__(self):
        return self.title


