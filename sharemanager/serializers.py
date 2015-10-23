from rest_framework import serializers
from sharemanager.models import ShareManager, XPUser


class ShareManagerSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = ShareManager
        fields = ('id', 'shareto', 'sharetoemail', 'data', 'expire', 'owner')

class UserSerializer(serializers.ModelSerializer):
    sharemanager = serializers.PrimaryKeyRelatedField(many=True, queryset=ShareManager.objects.all())

    class Meta:
        model = XPUser
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'gcm_token', 'sharemanager')
