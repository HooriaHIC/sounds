from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django import forms
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, Http404, HttpResponse
from django.template.response import TemplateResponse
from django.urls import reverse
from .models import Music, Playlist, Album, Like
from users.models import Profile, User
from .forms import MusicForm
from django.contrib.auth.decorators import login_required
import datetime


def home(request):
    return TemplateResponse(request, "home.html")


def albums(request):
    context = {
        'albums': Album.objects.all()
    }
    return TemplateResponse(request, 'albums.html', context)


def explore(request):
    today = datetime.date.today()
    context = {
        'music': Music.objects.all(),
        'playlist': Playlist.objects.all(),
        'latest': Music.objects.filter(date_posted__gt=today)
    }
    return TemplateResponse(request, "explore.html", context)


def nowplay(request):
    context = {
        'playlist': Playlist.objects.all(),
    }
    return TemplateResponse(request, "nowplay.html", context)


class MusicCreateView(LoginRequiredMixin, CreateView):
    model = Music
    fields = ['name', 'song', 'slug', 'lyrics', 'image', 'genre']

    def form_valid(self, form):
        form.instance.artist = self.request.user
        return super().form_valid(form)


class MusicDetailView(DetailView):
    model = Music


# @login_required
# def fav_update(request, slug):
# music = get_object_or_404(Music, slug=slug)
# music.fav = True if music.fav is False else False
# music.save(update_fields=['fav'])
# return redirect('fav')


# @login_required
# def FavView(request):
# context = {
# 'items': Music.objects.all().filter(fav=True)
# }
# return TemplateResponse(request, 'favorite.html', context)

@login_required
def like(request, song_id):
    new_like, created = Like.objects.get_or_create(
        user=request.user, song_id=song_id)
    if not created:
        Like.objects.filter(user=request.user, song_id=song_id).delete()
        return redirect('/explore')
    else:
        return redirect('/explore')


class MusicUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Music
    fields = fields = ['name', 'song', 'lyrics', 'image', 'genre']

    def form_valid(self, form):
        form.instance.artist = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.artist:
            return True
        return False


class MusicDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Music
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.artist:
            return True
        return False


class PlaylistCreateView(LoginRequiredMixin, CreateView):
    model = Playlist
    fields = ['name', 'songs', 'image']

    def form_valid(self, form):
        form.instance.artist = self.request.user
        return super().form_valid(form)


class PlaylistDetailView(DetailView):
    model = Playlist


class PlaylistUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Playlist
    fields = fields = ['name', 'songs', 'image']

    def form_valid(self, form):
        form.instance.artist = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.artist:
            return True
        return False


class PlaylistDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Playlist
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.artist:
            return True
        return False


@login_required
def add_to_playlist(request, operation, pk, playlist_id):
    playlist = Playlist.objects.get(pk=playlist_id)
    new_song = Music.objects.get(pk=pk)
    if operation == 'add':
        playlist.songs.add(new_song)
    elif operation == 'remove':
        playlist.songs.remove(new_song)
    return redirect('/')


class AlbumCreateView(LoginRequiredMixin, CreateView):
    model = Album
    fields = ['name', 'image', 'songs', 'slug', 'release_date']

    def form_valid(self, form):
        form.instance.artist = self.request.user
        return super().form_valid(form)


class AlbumDetailView(DetailView):
    model = Album


class AlbumUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Album
    fields = fields = ['name', 'image', 'songs', 'release_date']

    def form_valid(self, form):
        form.instance.artist = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.artist:
            return True
        return False


class AlbumDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Album
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.artist:
            return True
        return False


class MusicListView(ListView):
    model = Music
    template_name = 'core/music_list.html'
    context_object_name = 'music'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Music.objects.filter(artist=user)
