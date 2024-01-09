from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from annoying.decorators import ajax_request
import requests
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Favorite,Favoritemovies

#********************************************************   Home  ********************************************************************#

url = "https://api.themoviedb.org/3/movie/upcoming"
headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI4OGEwM2U5NWRhNmZhNzMyYzExZTU2ZTY5MzA1ZGRmZiIsInN1YiI6IjY1OGQ1OTY0ZjJjZjI1NzE1NDRjYzA2YiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.4zKSW7PO9ui7ipxLh055SGAcsSsnzDevKlzrLnN4rXk"
    }
response = requests.get(url, headers=headers).json()
details=[]
for i in range(20):
    id = response["results"][i]["id"]
    title = response["results"][i]["original_title"]
    desc = response["results"][i]["overview"][0:300]
    poster_path = response["results"][i]["poster_path"]
    poster_url = f'https://image.tmdb.org/t/p/original/{poster_path}'
    lst = [title,desc,poster_url,id]
    details.append(lst)

url2 = "https://api.themoviedb.org/3/movie/popular"
response2 = requests.get(url2, headers=headers).json()
popular=[]
for i in range(20):
    id = response2["results"][i]["id"]
    poster_path = response2["results"][i]["poster_path"]
    poster_url = f'https://image.tmdb.org/t/p/original/{poster_path}'
    popular.append([poster_url,id])

url3 = "https://api.themoviedb.org/3/movie/top_rated"
response3 = requests.get(url3, headers=headers).json()
top_rated=[]
for i in range(20):
    id = response3["results"][i]["id"]
    poster_path = response3["results"][i]["poster_path"]
    poster_url = f'https://image.tmdb.org/t/p/original/{poster_path}'
    top_rated.append([poster_url,id])

url4 = "https://api.themoviedb.org/3/trending/movie/day"
response4 = requests.get(url4, headers=headers).json()
trending=[]
for i in range(20):
    id = response4["results"][i]["id"]
    poster_path = response4["results"][i]["poster_path"]
    poster_url = f'https://image.tmdb.org/t/p/original/{poster_path}'
    trending.append([poster_url,id])

url5 = "https://api.themoviedb.org/3/trending/tv/day"
response5 = requests.get(url5, headers=headers).json()
tv=[]
for i in range(20):
    id = response5["results"][i]["id"]
    poster_path = response5["results"][i]["poster_path"]
    poster_url = f'https://image.tmdb.org/t/p/original/{poster_path}'
    tv.append([poster_url,id])

homepage={
    "details":details,
    "popular":popular,
    "top_rated":top_rated,
    "trending":trending,
    "tv":tv
    }

def home(request):
    return render(request,'home.html',homepage)

#********************************************************   Movies  ********************************************************************#

url6 = "https://api.themoviedb.org/3/genre/movie/list?"
response6 = requests.get(url6,headers=headers).json()
genre=[]
for i in response6["genres"]:
    list=[i["id"],i["name"]]
    genre.append(list)

def movie_list(request):
    movies = fetch_movies(page=1)
    return render(request, 'movies.html', {'movies': movies,"genre":genre})

@ajax_request
def load_more_movies(request, page):
    movies = fetch_movies(page=page)
    return {'movies': movies}

def fetch_movies(page):
    api_key = '88a03e95da6fa732c11e56e69305ddff'
    base_url = 'https://api.themoviedb.org/3/discover/movie'

    params = {
        'api_key': api_key,
        'page': page,
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        movies = data.get('results', [])
        return movies
    else:
        return []
    

#********************************************************   Tv Shows  ********************************************************************#

url7 = "https://api.themoviedb.org/3/genre/tv/list?"
response7 = requests.get(url7,headers=headers).json()
tv_genre=[]
for i in response7["genres"]:
    list=[i["id"],i["name"]]
    tv_genre.append(list)

def tv_list(request):
    tv = fetch_tv(page=1)
    return render(request, 'tvShows.html', {'tv': tv,"genre":tv_genre})

@ajax_request
def load_more_tv(request, page):
    tv = fetch_tv(page=page)
    return {'tv': tv}

def fetch_tv(page):
    api_key = '88a03e95da6fa732c11e56e69305ddff'
    base_url = 'https://api.themoviedb.org/3/discover/tv'

    params = {
        'api_key': api_key,
        'page': page,
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        tv = data.get('results', [])
        return tv
    else:
        return []



#********************************************************   Movie Filter  ********************************************************************#
def filtermovie_list(request,genre):
    filter_movies = fetch_filtermovie(page=1,genre=genre)
    return render(request, 'moviefilter.html', {'movies': filter_movies,"genre_name":genre})


@ajax_request
def load_more_filtermovie(request,page,genre):
    filter_movies = fetch_filtermovie(page=page,genre=genre)
    return {'movies': filter_movies}

def fetch_filtermovie(page,genre):

    api_key = '88a03e95da6fa732c11e56e69305ddff'
    base_url = 'https://api.themoviedb.org/3/discover/movie'

    genre_id = get_genre_id(api_key, genre)

    params = {
        'api_key': api_key,
        'sort_by': 'popularity.desc',
        'include_adult': 'true',
        'include_video': 'false',
        'page': page,
        'with_genres': genre_id,
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        filter_movies = data.get('results', [])
        return filter_movies
    else:
        print('Error fetching movies by genre:', response.text)
        return {'movies': []}


def get_genre_id(api_key, genre_name):
    genre_url = 'https://api.themoviedb.org/3/genre/movie/list'
    params = {'api_key': api_key, 'language': 'en-US'}
    response = requests.get(genre_url, params=params)

    if response.status_code == 200:
        data = response.json()
        genres = data.get('genres', [])
        for genre in genres:
            if genre['name'].lower() == genre_name.lower():
                return genre['id']

    print(f'Genre ID not found for {genre_name}')
    return None


#********************************************************   TV Filter  ********************************************************************#
def filtertv_list(request,genre):
    filter_tv = fetch_filtertv(page=1,genre=genre)
    return render(request, 'tvfilter.html', {'movies': filter_tv,"genre_name":genre})


@ajax_request
def load_more_filtertv(request,page,genre):
    filter_tv = fetch_filtertv(page=page,genre=genre)
    return {'movies': filter_tv}

def fetch_filtertv(page,genre):

    api_key = '88a03e95da6fa732c11e56e69305ddff'
    base_url = 'https://api.themoviedb.org/3/discover/tv'

    genre_id = get_genre_id(api_key, genre)

    params = {
        'api_key': api_key,
        'sort_by': 'popularity.desc',
        'include_adult': 'false',
        'include_video': 'false',
        'page': page,
        'with_genres': genre_id,
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        filter_tv = data.get('results', [])
        return filter_tv
    else:
        print('Error fetching Tv Shows by genre:', response.text)
        return {'movies': []}


def get_genre_id(api_key, genre_name):
    genre_url = 'https://api.themoviedb.org/3/genre/tv/list'
    params = {'api_key': api_key}
    response = requests.get(genre_url, params=params)

    if response.status_code == 200:
        data = response.json()
        genres = data.get('genres', [])
        for genre in genres:
            if genre['name'].lower() == genre_name.lower():
                return genre['id']

    print(f'Genre ID not found for {genre_name}')
    return None


#********************************************************   Movie Details  ********************************************************************#

def movieDetails(request,id):
    user = request.user
    movie_in_favorites=None
    if user.is_authenticated:
        movie_in_favorites = Favorite.objects.filter(user=user, tmdb_movie_id=id).exists()

    api_key = '88a03e95da6fa732c11e56e69305ddff'

    movie_url = f'https://api.themoviedb.org/3/movie/{id}'
    params = {'api_key': api_key}
    movie_response = requests.get(movie_url, params=params)
    movie_data = movie_response.json()

    trailer_url = f'https://api.themoviedb.org/3/movie/{id}/videos'
    trailer_response = requests.get(trailer_url, params=params)
    trailers = trailer_response.json().get('results', [])
    trailer_key = None
    for i in trailers:
        if i['type'] == 'Trailer':
            trailer_key = i['key']
            break    

    poster_path = movie_data["poster_path"]
    poster_url = f'https://image.tmdb.org/t/p/original/{poster_path}'

    images_url = f'https://api.themoviedb.org/3/movie/{id}/images'
    images_response = requests.get(images_url, params=params)
    images_data = images_response.json()
    backdrops = images_data.get('backdrops', [])[8:28]

    reviews_url = f'https://api.themoviedb.org/3/movie/{id}/reviews'
    reviews_response = requests.get(reviews_url, params=params)
    reviews_data = reviews_response.json()
    reviews = reviews_data.get('results', [])

    response_data = {
            'movie_details': movie_data,
            'trailers': trailer_key,
            'backdrops': backdrops,
            'reviews': reviews,
            'poster':poster_url,
            'movie_in_favorites': movie_in_favorites,
        }
    return render(request,"moviedetails.html",response_data)


#********************************************************   Tv Show Details  ********************************************************************#
def tvDetails(request,id):
    user = request.user
    movie_in_favorites=None
    if user.is_authenticated:
        movie_in_favorites = Favoritemovies.objects.filter(user=user, tmdb_tv_id=id).exists()
    
    api_key = '88a03e95da6fa732c11e56e69305ddff'

    movie_url = f'https://api.themoviedb.org/3/tv/{id}'
    params = {'api_key': api_key}
    movie_response = requests.get(movie_url, params=params)
    movie_data = movie_response.json()

    trailer_url = f'https://api.themoviedb.org/3/tv/{id}/videos'
    trailer_response = requests.get(trailer_url, params=params)
    trailers = trailer_response.json().get('results', [])
    trailer_key = None
    for i in trailers:
        if i['type'] == 'Trailer':
            trailer_key = i['key']
            break

    poster_path = movie_data["poster_path"]
    poster_url = f'https://image.tmdb.org/t/p/original/{poster_path}'


    images_url = f'https://api.themoviedb.org/3/tv/{id}/images'
    images_response = requests.get(images_url, params=params)
    images_data = images_response.json()
    backdrops = images_data.get('backdrops', [])[8:28]

    reviews_url = f'https://api.themoviedb.org/3/tv/{id}/reviews'
    reviews_response = requests.get(reviews_url, params=params)
    reviews_data = reviews_response.json()
    reviews = reviews_data.get('results', [])

    response_data = {
            'movie_details': movie_data,
            'trailers': trailer_key,
            'backdrops': backdrops,
            'reviews': reviews,
            'poster':poster_url,
            'movie_in_favorites': movie_in_favorites,
        }
    return render(request,"tvDetails.html",response_data)


#********************************************************   Search Bar  ********************************************************************#

def searchResult(request):
    dataset = request.POST.get("search-bar",'default')
    api_key = '88a03e95da6fa732c11e56e69305ddff'
    url = 'https://api.themoviedb.org/3/search/multi'
    params = {'api_key': api_key, 'query': dataset, 'language': 'en-US'}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        results = data.get('results', [])
        movie=False
        tv_shows=False
        for i in results:
            if i['media_type'] == 'movie':
                movie=results
                tv_shows = False
            elif i['media_type'] == 'tv':
                tv_shows=results
                movie = False
        if movie==False and tv_shows==False:
            data="none"
            keys="none"

        else:
            if movie!=False:
                data=movie
                keys = data[0].keys()

            if tv_shows!=False:
                data=tv_shows
                keys = data[0].keys()  

    else:
        print("Error")
    
    return render(request,'search.html',{'data':data,'keys':keys})


#********************************************************  Dashboard  ********************************************************************#
def dashboard(request):
    user = request.user
    if user.is_authenticated:
        favorites = Favorite.objects.filter(user=user)
        favtv = Favoritemovies.objects.filter(user=user)
        movie_name=[]
        tv_name=[]
        for i in favorites:
            name = get_movie_name(i.tmdb_movie_id)
            movie_name.append(name)
        for i in favtv:
            name = get_tv_name(i.tmdb_tv_id)
            tv_name.append(name)
        return render(request, 'profile.html', {'favorites': movie_name,"favoritetv":tv_name})
    else:
        return render(request,'profile.html')


def get_movie_name(id):
    api_key = '88a03e95da6fa732c11e56e69305ddff'
    movie_url = f'https://api.themoviedb.org/3/movie/{id}'
    params = {'api_key': api_key}
    movie_response = requests.get(movie_url, params=params)
    movie_data = movie_response.json() 
    return movie_data["title"]

def get_tv_name(id):
    api_key = '88a03e95da6fa732c11e56e69305ddff'
    movie_url = f'https://api.themoviedb.org/3/tv/{id}'
    params = {'api_key': api_key}
    movie_response = requests.get(movie_url, params=params)
    movie_data = movie_response.json() 
    return movie_data["name"]

#********************************************************   Login-system  ********************************************************************#
def userlogin(request):
    if request.method == 'POST':
        uname = request.POST.get("Username")
        password = request.POST.get("pass")
        user = authenticate(request,username=uname,password=password)
        print(uname,password,user)
        if user is not None:
            login(request,user)
            return redirect("home")
        else:
            mess="Login failed! Incorrect Username or Password"
            return render(request,'login.html',{"mess":mess})
    return render(request,'login.html')

def register(request):
    if request.method == 'POST':
        uname = request.POST.get("Username")
        email = request.POST.get("email")
        first = request.POST.get("firstname")
        last = request.POST.get("lastname")
        pass1 = request.POST.get("pass")
        pass2 = request.POST.get("confirm")
        if uname or email or first or last or pass1 or pass2 == "":
            mess = "Please enter all the necessary fields!!"
            return render(request,"signUp.html",{"mess":mess})

        if User.objects.filter(username=uname).exists():
            mess = "Username already exist!!"
            return render(request,"signUp.html",{"mess":mess})
        
        if pass1 != pass2:
            mess = "You entered different passwords!!"
            return render(request,"signUp.html",{"mess":mess})
        
        try:
            my_user = User.objects.create_user(first_name=first,last_name=last,username=uname, email=email,password= pass1)
            my_user.save()
            return HttpResponse("User Created Successfully")
        except:
            return HttpResponse("Error creating user. Please try again.")
    return render(request,'signUp.html')

def userlogout(request):
    logout(request)
    return redirect("home")


#********************************************************   Favourite movies ans shows  ********************************************************************#
@login_required
def add_to_favorites(request, tmdb_movie_id):
    user = request.user    
    try:
        movie = Favorite.objects.get(user=user, tmdb_movie_id=tmdb_movie_id)
        movie.delete()
    except Favorite.DoesNotExist:
        Favorite.objects.create(user=user, tmdb_movie_id=tmdb_movie_id)
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    else:
        return redirect('movieDetails', id=tmdb_movie_id)


@login_required
def add_to_favorites_tv(request, tmdb_tv_id):
    user = request.user
    try:
        movie=Favoritemovies.objects.get(user=user,tmdb_tv_id=tmdb_tv_id)
        movie.delete()
    except Favoritemovies.DoesNotExist:
        Favoritemovies.objects.create(user=user, tmdb_tv_id=tmdb_tv_id)
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    else:
        return redirect('movieDetails', id=tmdb_tv_id)