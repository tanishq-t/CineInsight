from django.contrib import admin

from .models import Favorite
admin.site.register(Favorite)

from .models import Favoritemovies
admin.site.register(Favoritemovies)

