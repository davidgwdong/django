from rest_framework import serializers
from sharemanager.models import ShareManager
from django.contrib.auth.models import User


class ShareManagerSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = ShareManager
        fields = ('id', 'datauuid', 'owneruuid', 'sharetouuid', 'sharetoemail', 'data', 'expire', 'owner')

class UserSerializer(serializers.ModelSerializer):
    sharemanager = serializers.PrimaryKeyRelatedField(many=True, queryset=ShareManager.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'sharemanager')
