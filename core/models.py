from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='Profile/', verbose_name="Profile Picture", blank=True, null=True, default=None)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=255, verbose_name="City", blank=True, null=True)
    state = models.CharField(max_length=255, verbose_name="State", blank=True, null=True)
    pincode = models.PositiveBigIntegerField(verbose_name="Pincode", blank=True, null=True)
    
    def __str__(self):
        return self.user.username


CATOGORIES = (
    ("Mental Health", "Mental Health"),
    ("Heart Disease", "Heart Disease"),
    ("Covid19", "Covid19"),
    ("Immunization", "Immunization"),
)

class Blog(models.Model):
    user = models.ForeignKey(User, verbose_name="Author", on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name="Blog Title")
    image = models.ImageField(upload_to='blog/', verbose_name="Blog Image")
    cat = models.CharField(choices=CATOGORIES, default=0, max_length=100, verbose_name="Category")
    summary = models.TextField()
    content = models.TextField()
    is_draft = models.BooleanField(default=False)
    comments = models.ManyToManyField('Comments', blank=True)
    likes = models.ManyToManyField(User, blank=True, related_name='liked_user')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def count_comments(self):
        return self.comments.count()

    def count_likes(self):
        return self.likes.count()

    def add_like(self, user):
        if self.likes.filter(id=user.id).exists():
            self.likes.remove(user)
        else:
            self.likes.add(user)
        self.save()
        return True

    def __str__(self):
        return self.title.capitalize()


class Comments(models.Model):
    user = models.ForeignKey(User, verbose_name="Author", on_delete=models.CASCADE)
    text = models.TextField(max_length=255, verbose_name="Comment")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    speciality = models.CharField(max_length=100)
    is_doctor = models.BooleanField(default=True)
    def __str__(self):
        return self.user.get_full_name()

class Appointment(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    cause = models.CharField(max_length=255,verbose_name="Causes")
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    is_visited = models.BooleanField(default=False)
    
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.patient} - {self.doctor} on {self.date} at {self.start_time}"
    
    
    def is_expired(self):
        appointment_datetime = datetime.combine(self.date, self.end_time)
        appointment_datetime = timezone.make_aware(appointment_datetime, timezone.get_current_timezone())
        return timezone.now() > appointment_datetime
    
# Signals
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()
