from rest_framework import serializers
from .models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

class UserLoginSerializer(serializers.Serializer):
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, instance):
        first_name = instance.get('first_name', '')
        last_name = instance.get('last_name', '')
        if first_name and last_name:
            return f"{first_name} {last_name}"
        elif first_name:
            return first_name
        elif last_name:
            return last_name
        else:
            return ""
