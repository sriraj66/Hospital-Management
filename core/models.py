from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='Profile/', verbose_name="Profile Picture", blank=True, null=True, default=None)
    
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=255, verbose_name="City", blank=True, null=True)
    state = models.CharField(max_length=255, verbose_name="State", blank=True, null=True)
    pincode = models.PositiveBigIntegerField(verbose_name="Pincode", blank=True, null=True)
    
    def __str__(self):
        return self.user.username

# Signals 
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()