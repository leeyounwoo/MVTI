from django.shortcuts import render, redirect
import requests
import json
from .models import Movie, Genre, Ott, Tournament, Review
import csv
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import MovieSerializer, TournamentSerializer, MovieDetailSerializer, ReviewSerializer
from django.http.response import JsonResponse
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

# from rest_framework_jwt.authentication import JSONWebTokenAuthentication

@api_view(['GET'])
def index(request) :
    netflix = Ott.objects.get(name = 'Netflix')
    netflix_movies = Movie.objects.filter(movie_ott = netflix).order_by('-popularity')[:20]
    disney = Ott.objects.get(name = 'Disney Plus')
    disney_movies = Movie.objects.filter(movie_ott = disney).order_by('-popularity')[:20]
    amazon = Ott.objects.get(name = 'Amazon Prime')
    amazon_movies = Movie.objects.filter(movie_ott = amazon).order_by('-popularity')[:20]
    hulu = Ott.objects.get(name = 'Hulu')
    hulu_movies = Movie.objects.filter(movie_ott = hulu).order_by('-popularity')[:20]
    popular_movies = Movie.objects.order_by('-vote_cnt')[:20]
    # latest_movies = Movie.objects.order_by('-released_date')[:20]
    # highscore_movies = Movie.objects.order_by('-vote_average')[:20]
    netflix_serializer = MovieSerializer(data=netflix_movies, many=True)
    disney_serializer = MovieSerializer(data=disney_movies, many=True)
    amazon_serializer = MovieSerializer(data=amazon_movies, many=True)
    hulu_serializer = MovieSerializer(data=hulu_movies, many=True)
    popular_serializer = MovieSerializer(data=popular_movies, many=True)
    # latest_serializer = MovieSerializer(data=latest_movies, many=True)
    # highscore_serializer = MovieSerializer(data=highscore_movies, many=True)
    # like_serializer = MovieSerializer(data=like_movies, many=True)
    print(netflix_serializer.is_valid(), disney_serializer.is_valid(), amazon_serializer.is_valid(), hulu_serializer.is_valid(), \
        popular_serializer.is_valid(), ) 
    # print(latest_serializer.is_valid() , highscore_serializer.is_valid() , like_serializer.is_valid())
    
    context={
        'netflix_movies' : netflix_serializer.data,
        'disney_movies' : disney_serializer.data,
        'amazon_movies' : amazon_serializer.data,
        'hulu_movies' : hulu_serializer.data,
        'popular_movies' : popular_serializer.data,
        # 'latest_movies' : latest_serializer.data,
        # 'highscore_movies' : highscore_serializer.data,
    }
    return JsonResponse(context)

# def detail(request, movie_pk):
#     movie = Movie.objects.get(pk=movie_pk)
#     url = f'https://api.themoviedb.org/3/movie/{movie.idx}/similar?api_key=1b7edbdee7b82ec37e80ba4d2b36db68&language=ko-KR&page=1'
#     res = requests.get(url)
#     similars = res.json().get('results')
#     movies = []
#     for similar in similars:
#         movie = Movie.objects.filter(title = similar['title'], released_date = similar['release_date']).first()
#         if movie != None:
#             movies.append(movie)
#             print(movie.title)
#     context={
#         'similar_movies' : movies
#     }
#     return render(request, 'movies/detail.html', context)



@api_view(['GET'])
def movie_detail(request, movie_pk) :
    movie = Movie.objects.get(pk=movie_pk)
    movie_list = [movie]
    # serializer = MovieDetailSerializer(data = movie)
    serializer = MovieDetailSerializer(data = movie_list, many=True)

    # 한영화의 genres에 포함된 genre를 포함하는 genres를 가지고 있는 영화들을 찾고 싶다. - 해결
    
    # genres = movie.genres.all().values_list('id', flat=True) # 영화의 모든 genre를 id 객체로 가져오기
    # movies_same_genre = Movie.objects.filter(genres__id__in=genres).order_by('-vote_count').distinct()[:20]

    # recommended_movies = Movie.objects.filter(genres = movie.genres.all())[:10]
    # same_genre_serializer = MovieDetailSerializer(data = movies_same_genre, many=True)
    print(serializer.is_valid())
    # print(same_genre_serializer.is_valid())
    context = {
        "movie" : serializer.data, 
        # "same_genres" : same_genre_serializer.data,
    }

    # movieSerializer = MovieSerializer(data = recommended_movies, many=True)
    return Response(context)



def add_genre(request):
    url = "https://api.themoviedb.org/3/genre/movie/list?api_key=1b7edbdee7b82ec37e80ba4d2b36db68"
    res = requests.get(url)
    infos = res.json().get('genres')
    for i in range(len(infos)):
        Genre(
            genre_id = infos[i]['id'],
            genre_name = infos[i]['name'],
        ).save()
    return redirect('recruits:index')

def add_info(request):
    for page in range(1, 50):
        url = "https://api.themoviedb.org/3/movie/popular?api_key=1b7edbdee7b82ec37e80ba4d2b36db68&language=ko-KR&page=" + str(page)
        res = requests.get(url)
        infos = res.json().get('results')
        for i in range(len(infos)):
            if not infos[i]["poster_path"] or not infos[i]['title'] or not infos[i]['overview'] or not infos[i]['release_date'] or not infos[i]['vote_count'] or not infos[i]['genre_ids']:
                continue

            # print( infos[i]['title'],
            #     infos[i]['overview'],
            #     infos[i]['release_date'],
            #     infos[i]['poster_path'])
            # print(infos[i]['popularity'],
            #     infos[i]['vote_average'],
            #     infos[i]['vote_count'])
        
            Movie(
                idx = infos[i]['id'],
                title = infos[i]['title'],
                eng_title = infos[i]['original_title'],
                overview = infos[i]['overview'],
                released_date = infos[i]['release_date'],
                poster_path = infos[i]['poster_path'],
                popularity = infos[i]['popularity'],
                vote_average = infos[i]['vote_average'],
                vote_cnt = infos[i]['vote_count'],
            ).save()
            genres = infos[i]['genre_ids']
            movie = Movie.objects.get(title = infos[i]['title'], released_date = infos[i]['release_date'])
            for j in range(len(genres)):
                genre = Genre.objects.get(genre_id = genres[j])
                movie.movie_genre.add(genre)
    return redirect('recruits:index')

def ott_info(request):
    path1 = 'C:/Users/Lee/Desktop/pro/WTT/netflix_titles.csv'
    path2 = 'C:/Users/Lee/Desktop/pro/WTT/disney_plus_titles.csv'
    path3 = 'C:/Users/Lee/Desktop/pro/WTT/amazon_prime_titles.csv'
    path4 = 'C:/Users/Lee/Desktop/pro/WTT/hulu_titles.csv'

    file = open(path1, 'rt', encoding='UTF8')
    reader = csv.reader(file)
    for row in reader:
        title = row[2]
        movie = Movie.objects.filter(eng_title = title).first()
        if movie != None:
            print(movie.title)
            ott = Ott.objects.get(name = 'Netflix')
            movie.movie_ott.add(ott)

    file = open(path2, 'rt', encoding='UTF8')
    reader = csv.reader(file)
    for row in reader:
        title = row[2]
        movie = Movie.objects.filter(eng_title = title).first()
        if movie != None:
            print(movie.title)
            ott = Ott.objects.get(name = 'Disney Plus')
            movie.movie_ott.add(ott)

    file = open(path3, 'rt', encoding='UTF8')
    reader = csv.reader(file)
    for row in reader:
        title = row[2]
        movie = Movie.objects.filter(eng_title = title).first()
        if movie != None:
            print(movie.title)
            ott = Ott.objects.get(name = 'Amazon Prime')
            movie.movie_ott.add(ott)

    file = open(path4, 'rt', encoding='UTF8')
    reader = csv.reader(file)
    for row in reader:
        title = row[2]
        movie = Movie.objects.filter(eng_title = title).first()
        if movie != None:
            print(movie.title)
            ott = Ott.objects.get(name = 'Hulu')
            movie.movie_ott.add(ott)
    return redirect('recruits:index')    


@api_view(['GET', 'POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def tournament(request) :
    if request.method == 'GET' :
        random_movies = Movie.objects.order_by('?')[:16]
        serializer = MovieSerializer(data = random_movies, many=True)
        print(serializer.is_valid())
        return Response(serializer.data)
    elif request.method =='POST' : 
        # 작업중
        movie_id = request.data["movie_id"]
        user = request.user
        print(user)
        movie = Movie.objects.get(pk=movie_id)
        tournament = Tournament.objects.create(
            movie = movie, 
            user = request.user
        )

        serializer = TournamentSerializer(data= tournament)
        print(serializer.is_valid())
        return Response(serializer.data)


@api_view(['GET'])
def mypageMovie(request, username) :
    person = get_object_or_404(get_user_model(), username=username)
    winMovies = Movie.objects.filter(tournament__user=person).distinct() # OneToMany 접근
    # likeMovies = Review.objects.filter(user=person).filter(liked=True).order_by('-created_at')
    # likeMovies = Movie.objects.filter(review__user=person).distinct()

    winMoviesSerializer = MovieSerializer(data = winMovies, many=True)
    # likeMoviesSerializer = MovieSerializer(data= likeMovies, many=True)

    print(winMoviesSerializer.is_valid())
    context = {
        'winMovies' : winMoviesSerializer.data, 
        # 'likeMovies' : likeMoviesSerializer.data
    }
    return Response(context)

@api_view(['POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def review_create(request, movie_pk):
    print(request.data)
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user, movie=movie)
        print('123')
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def review_delete(request, movie_pk, review_pk):
    if not request.user.movie_reviews.filter(pk=review_pk).exists():
        return Response({'detail': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
    
    
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == 'DELETE':
        review.delete()
        return Response({'id':review_pk}, status=status.HTTP_204_NO_CONTENT)


