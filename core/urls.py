from django.urls import path, include
from .views import *


urlpatterns = [
    path('', home, name="home"),
    path('albums/', albums, name="albums"),
    path('fav/<song_id>/', like, name='like'),
    path('music/<str:username>', MusicListView.as_view(), name='music-list'),
    path('explore/', explore, name='explore'),
    path('post/<int:pk>/delete/', MusicDeleteView.as_view(), name='post-delete'),
    path('new/', MusicCreateView.as_view(), name='post-create'),
    path('playlists/', nowplay, name='playing'),
    path('post/<int:pk>/', MusicDetailView.as_view(), name='post-detail'),
    # path('favorites/', FavView, name='fav'),
    path('post/<int:pk>/update/', MusicUpdateView.as_view(), name='post-update'),
    path('playlist/<int:pk>/delete/',
         PlaylistDeleteView.as_view(), name='playlist-delete'),
    path('new_playlist/', PlaylistCreateView.as_view(), name='playlist-create'),
    path('playlist/<int:pk>/', PlaylistDetailView.as_view(), name='playlist-detail'),
    path('playlist/<int:pk>/update/',
         PlaylistUpdateView.as_view(), name='playlist-update'),
    path('new_album/', AlbumCreateView.as_view(), name='album-create'),
    path('album/<int:pk>/', AlbumDetailView.as_view(), name='album-detail'),
    path('album/<int:pk>/update/',
         AlbumUpdateView.as_view(), name='album-update'),
    path('album/<int:pk>/delete/',
         AlbumDeleteView.as_view(), name='album-delete'),
    path('add_to_playlist/<operation>/<pk>/<playlist_id>',
         add_to_playlist, name="add_to_playlist"),
]
