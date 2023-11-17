from django.urls import path
from api.views import upload_to_google_drive

urlpatterns = [
    path('upload/', upload_to_google_drive, name='upload_to_google_drive'),
]