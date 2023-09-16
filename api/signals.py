from django.dispatch import receiver
from .models import *
from django.db.models.signals import post_save

# @receiver(pre_save,sender=MyUser)
# def doctor_insatance(sender,instance,created,*args,**kwargs):
#      if instance.is_doctor and not instance.pk:
#         Doctor.objects.create(user=instance)


@receiver(post_save,sender=MyUser)
def creating_doctor_instance(sender,instance,created,*args,**kwargs):
    if created and instance.is_doctor:
        Doctor.objects.create(user=instance)