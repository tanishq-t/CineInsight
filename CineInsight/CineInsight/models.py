from django.db import models
from django.contrib.auth.models import User

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tmdb_movie_id = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.tmdb_movie_id}"

    class Meta:
        app_label = 'CineInsight'

class Favoritemovies(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tmdb_tv_id = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.tmdb_tv_id}"

    class Meta:
        app_label = 'CineInsight'

