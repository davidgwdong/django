from django.db import models


class ShareManager(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    datauuid = models.UUIDField()
    owneruuid = models.UUIDField()
    sharetouuid = models.UUIDField()
    sharetoemail = models.EmailField()
    data = models.URLField()
    expire = models.DateTimeField()
    owner = models.ForeignKey('auth.User', related_name='sharemanager')

    class Meta:
        ordering = ('created',)
