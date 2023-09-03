from django.shortcuts import render
from django.contrib.auth.models import User
from knox.auth import AuthToken
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
import requests
from .serializers import SignupSerializer, FilesSerializer
from .models import Files
from .encryption_utils import encrypt, decrypt

# Create your views here.

@api_view(['POST'])
def signup_api(request):
    
    """
    This is for user Signup.
    
    Required: Username, Email, Password
    
    Return: User information and the token created
    """
    
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        success, token = AuthToken.objects.create(user)
        
        return Response({
            'user':{
                'id': user.id,
                'username': user.username,
                'email': user.email
            },
            'token': token,
            'success': True
        })
        
    return Response({
        'success': False
    })
    
@api_view(['POST'])
def login_api(request):
    
    """
    This is for Login.
    
    Required: Username, Password.
    
    Username -> always unique.
    
    Return: User information and token.
    """
    serializer = AuthTokenSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        success,token = AuthToken.objects.create(user)
        return Response({
            'user':{
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'opertaion_user': user.is_staff
            },
            'token': token,
            'success': True
        })
        
    return Response({
        'success': False
    })
    
@api_view(['POST'])
def upload_file(request):
    
    """
    This is for Uploading Files.
    
    Required: File, User.
    
    File -> only xlsx, docx and pptx allowed.
    User -> only operation user are allowed.
    
    Returns: Response success if created else the error.
    """
    
    data = request.data
    user_id = int(data['user'])
    
    accepted_user = [user.id for user in User.objects.filter(is_staff=True)]
    if user_id in accepted_user:
        serializer = FilesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'success'
            })
        return Response("Only pptx, docx and xlsx files are allowed")
    
    return Response({"Only Operation User are allowed to upload files"})

@api_view(['GET'])
def get_files(request):
    
    """
    This take get requests and give all the files as response.
    
    Return: Files.
    """
    fields = ('file')
    files = Files.objects.all().only(fields)
    serializer = FilesSerializer(files, many=True)
    print(serializer)
    return Response(serializer.data)

@api_view(['POST'])
def download_file(request):
    
    """
    This is for getting download link.
    
    Returns: download link for file download.
    """
    
    data = request.data
    encrypted_id = encrypt(data['id'])
    encrypted_url = 'http://127.0.0.1:8000/api/download/'+encrypted_id
    return Response({
        'download-link': encrypted_url,
        'message': 'success'
    })
    
@api_view(['GET'])
def download_allowed(request,val):  # val is encrypted file id, coming from "path('download/<val>/',views.download)" in urls.py
    
    """
    This is  for checking that the user with download link is client or not.
    
    Required: Username
    
    Username(Unique) -> helps in validating the current user is allowed to dowload the file or not.
    """
    
    data = request.data
    user = data['user']
    allowed_user = [user.username for user in User.objects.filter(is_staff=False)]
    if user in allowed_user:
        decrypted_key = decrypt(val)
        file_obj = Files.objects.get(id=decrypted_key)
        url = 'http://127.0.0.1:8000/media/' + str(file_obj.file)
        file_name = 'file-dowload'
        with requests.get(url) as req:
            with open(file_name, 'wb') as f:
                for chunk in req.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        
            return Response("success")
        
    return Response({
        'messaage': 'Access Denied'
    })
        