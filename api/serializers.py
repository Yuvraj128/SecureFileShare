from django.contrib.auth.models import User
from rest_framework import serializers,validators
from .models import Files

class SignupSerializer(serializers.ModelSerializer):
    
    """
    This is for new user registration. 
    
    """
    
    class Meta:
        model = User
        fields = ('username','email','password')
        
        extra_kwargs = {
            'username': {
                'required': True,
                'validators': [
                    validators.UniqueValidator(
                        User.objects.all(), "User already exist with this username."
                    )
                ]
            },
            'password': {
                'required': True,
                'write_only': True
                         },
            'email': {
                'required': True,
                'validators': [
                    validators.UniqueValidator(
                        User.objects.all(), "User already exist with this email."
                    )
                ]
            }
        }
    
    def create(self, validated_data):
        username = validated_data.get('username')
        email = validated_data.get('email')
        password = validated_data.get('password')
        
        user = User.objects.create_user(
            username=username,
            email = email,
            password = password
        )
    
        return user


class FilesSerializer(serializers.ModelSerializer):
    """
    This serializes the file and create a file in database also.
    
    """
    class Meta:
        model = Files
        fields = ('file', 'user')
        
        extra_kwargs = {
            'file': {
                'required': True,
            }
        }
        
        
    def create(self,file_data):
        user = file_data.get('user')
        file = file_data.get('file')
        file_return = Files.objects.create(
            user = user,
            file = file
        )
        
        return file_return