from django.db import models
from django.contrib.auth.models import AbstractUser

class ShareManager(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    shareto = models.CharField(max_length=30)
    sharetoemail = models.EmailField()
    data = models.FileField()
    expire = models.DateTimeField()
    owner = models.ForeignKey('sharemanager.XPUser', related_name='sharemanager')

    class Meta:
        ordering = ('created',)

class XPUser(AbstractUser):
    gcm_token = models.CharField(max_length=300)
    # to enforce that you require email field to be associated with
    # every user at registration
    REQUIRED_FIELDS = ["email"]
