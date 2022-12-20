from django.shortcuts import render
from django.contrib.auth import get_user_model
# Rest Framework imports
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

# Create your views here.

class RegisterSerializer(serializers.Serializer):
    email    = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=CustomUser.objects.all(), message=message.messages['User']['EmailExist'], lookup='iexact')])
    password = serializers.CharField(max_length=50, min_length=6, write_only=True, style={'input_type': 'password'})

    class Meta:
        # model = CustomUser
        fields = ['email', 'password']
        

    def validate(self, attrs):
        user = CustomUser(**attrs)

        # get the password from the attrs
        password = attrs.get('password')

        # errors = dict() 
        # try:
        #     # validate the password and catch the exception
        #     validators.validate_password(password=password, user=CustomUser)

        # # the exception raised here is different than serializers.ValidationError
        # except exceptions.ValidationError as e:
        #     errors['password'] = list(e.messages)

        # if errors:
        #     raise serializers.ValidationError(errors)

        return super(RegisterSerializer, self).validate(attrs)

    def create(self, validated_data):
        try:
            user = CustomUser.objects.get(email=validated_data['email'])
            raise serializers.ValidationError({"Error": message.messages['User']['EmailExist']})
        except CustomUser.DoesNotExist:
            user = CustomUser.objects.create_user(**validated_data)
            Token.objects.create(user=user)
        return user

