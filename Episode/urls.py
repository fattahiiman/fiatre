from django.urls import path
from .views import *

urlpatterns = [
    path('', EpisodesList.as_view(), name='episodes'),
    path('create/', EpisodesCreate.as_view(), name='episodes-create'),
    path('update/<pk>/', EpisodesUpdate.as_view(), name='episodes-update'),
    path('delete/<pk>/', EpisodesDelete.as_view(), name='episodes-delete'),
    path('video/delete/<pk>/', DeleteEpisodeVideo.as_view(), name='episodes-video-delete'),

    path('downloads', EpisodeDownloadsList.as_view(), name='episode_downloads'),
]
