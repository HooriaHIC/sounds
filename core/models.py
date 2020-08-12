from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone


User = get_user_model()

# Create your models here.


GENRE = [
    ('RK', 'Rock'),
    ('HIHO', 'Hip Hop'),
    ('J', 'Jazz'),
    ('C', 'Country'),
    ('B', 'Blues'),
    ('P', 'Pop'),
    ('S', 'Soul'),
    ('M', 'Metal'),
    ('D', 'Disco'),
    ('CL', 'Classical'),
    ('E', 'Electrodance'),
    ('R', 'Rap'),
    ('IP', 'Indie Pop'),
    ('K', 'K-Pop'),
    ('EM', 'Emo'),
    ('O', 'Opera'),
]


class Music(models.Model):
    image = models.ImageField()
    name = models.CharField(max_length=100, unique=True)
    song = models.FileField(upload_to='musics/', blank=False, null=False)
    artist = models.ForeignKey(User, on_delete=models.CASCADE)
    fav = models.BooleanField(default=False)
    slug = models.SlugField(unique=True)
    date_posted = models.DateTimeField(default=timezone.now)
    lyrics = models.TextField(default="Unknown lyrics")
    genre = models.CharField(
        max_length=300,
        choices=GENRE,
        null=False,
        blank=False,
        default=""
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class Album(models.Model):
    name = models.CharField(max_length=100)
    release_date = models.DateField(default=timezone.now)
    image = models.ImageField()
    songs = models.ManyToManyField(Music, null=True, blank=True)
    artist = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('playlist-detail', kwargs={'pk': self.pk})


class Playlist(models.Model):
    image = models.ImageField()
    name = models.CharField(max_length=100, unique=True)
    artist = models.ForeignKey(User, on_delete=models.CASCADE)
    songs = models.ManyToManyField(Music, null=True, blank=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('playlist-detail', kwargs={'pk': self.pk})

    @classmethod
    def add_music(cls, new_song):
        playlist, created = cls.objects.get_or_create(songs=new_song)
        playlist.songs.add(new_song)

    @classmethod
    def remove_music(cls, new_song):
        playlist, created = cls.objects.get_or_create(songs=new_song)
        playlist.songs.remove(new_song)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Music, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
