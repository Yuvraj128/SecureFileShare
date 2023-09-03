from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.login_api),
    path('signup/',views.signup_api),
    path('upload_file/',views.upload_file),
    path('download-file/',views.download_file),
    path('files/',views.get_files),
    path('download/<val>',views.download_allowed)
]