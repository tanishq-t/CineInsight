"""
URL configuration for CineInsight project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from CineInsight import views
from django.urls import path, include
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name="home"),
    path('accounts/', include('allauth.urls')),
    path('dashboard/',views.dashboard,name="dashboard"),
    path('login/',views.userlogin,name="login"),
    path('movies/', views.movie_list, name='movie_list'),
    path('load_more_movies/<int:page>/', views.load_more_movies, name='load_more_movies'),
    path('tv/', views.tv_list, name='tv_list'),
    path('load_more_tv/<int:page>/', views.load_more_tv, name='load_more_tv'),
    path('movies/<str:genre>/',views.filtermovie_list,name='filtermovie_list'),
    path('movies/<str:genre>/load_more/<int:page>/', views.load_more_filtermovie, name='load_more_filtermovie'),
    path('tv/<str:genre>/',views.filtertv_list,name='filtertv_list'),
    path('tv/<str:genre>/load_more/<int:page>/', views.load_more_filtertv, name='load_more_filtertv'),
    path('moviedetails/<int:id>',views.movieDetails,name="movieDetails"),
    path('tvdetails/<int:id>',views.tvDetails,name="tvDetails"),
    path('searchresult/',views.searchResult,name="searchResult"),
    path('register/',views.register,name="register"),
    path('logout/',views.userlogout,name="logout"),
    path('favourites/<int:tmdb_movie_id>',views.add_to_favorites,name="favourite"),
    path('favourite/<int:tmdb_tv_id>',views.add_to_favorites_tv,name="favouritetv")
]
