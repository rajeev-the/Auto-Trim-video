from django.urls import path
from .views import receive_data,download_video

urlpatterns = [
    path('data/', receive_data),
    path('download/<str:file_name>/', download_video, name='download_video'),
]
