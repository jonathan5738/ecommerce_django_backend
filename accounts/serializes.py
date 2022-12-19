from rest_framework import serializers 
from django.contrib.auth.models import User 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'write_only': True},
            'first_name': {'write_only': True},
            'last_name': {'write_only': True},
            'email': {'write_only': True}
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password); user.save()
        return user

    def update(self, inst, validated_data):
        inst.username = validated_data.get('username', inst.username)
        inst.first_name = validated_data.get('first_name', inst.first_name)
        inst.last_name = validated_data.get('last_name', inst.last_name)
        inst.email = validated_data.get('email', inst.email)
        inst.save()
        return inst


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=50)