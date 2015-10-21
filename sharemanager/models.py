from django.db import models


class ShareManager(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    shareto = models.CharField(max_length=30)
    sharetoemail = models.EmailField()
    data = models.FileField(upload_to='data')
    expire = models.DateTimeField()
    owner = models.ForeignKey('auth.User', related_name='sharemanager')

    class Meta:
        ordering = ('created',)
