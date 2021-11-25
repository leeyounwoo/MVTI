from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
import requests
import json
from .models import Movie, Genre, Ott, Tournament, Review
import csv
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import serializers, status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import MovieSerializer, TournamentSerializer, MovieDetailSerializer, ReviewSerializer
from django.http.response import JsonResponse
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

# from rest_framework_jwt.authentication import JSONWebTokenAuthentication

@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
def index(request) :
    person = get_object_or_404(get_user_model(), username=request.user)
    print(request.user)
    temp_movies = Movie.objects.filter(tournament__user=person).distinct()
    if len(temp_movies) == 0:
        mvti_movies = Movie.objects.all().order_by('-vote_cnt')[:20]
    elif len(temp_movies) == 1:
        if len(temp_movies[0].movie_genre.all()) < 2:
            mvti_movies = Movie.objects.filter(movie_genre = temp_movies[0].movie_genre.all()[0]).order_by('-popularity')[:20]
        else:
            mvti_movies = Movie.objects.filter(movie_genre = temp_movies[0].movie_genre.all()[0]).order_by('-popularity')[:10]
            for i in range(1, len(temp_movies[0].movie_genre.all())):
                gmovies = Movie.objects.filter(movie_genre = temp_movies[0].movie_genre.all()[i]).order_by('-popularity')[:10]
                mvti_movies = (mvti_movies | gmovies).order_by('-popularity')[:20]
    elif len(temp_movies) > 1:
        temp = {}
        for tmovie in temp_movies:
            print(tmovie.movie_genre.all())
            for genre in tmovie.movie_genre.all():
                if genre in temp:
                    temp[genre] += 1
                else:
                    temp[genre] = 1 
        temp = sorted(temp.items(), key = lambda x: x[1], reverse=True)
        print(temp)
        mvti_movies = Movie.objects.filter(movie_genre = temp[0][0]).order_by('-popularity')[:10]
        print(mvti_movies)
        if len(temp) == 1:
            mvti_movies = Movie.objects.filter(movie_genre = temp[0][0]).order_by('-popularity')[:20]
        else:
            for i in range(1, 3):
                gmovies = Movie.objects.filter(movie_genre = temp[i][0]).order_by('-popularity')[:10]
                print(gmovies)
                mvti_movies = (mvti_movies | gmovies).order_by('-popularity')
        print(mvti_movies)
    
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
    mvti_serializer = MovieSerializer(data=mvti_movies, many=True)
    # latest_serializer = MovieSerializer(data=latest_movies, many=True)
    # highscore_serializer = MovieSerializer(data=highscore_movies, many=True)
    # like_serializer = MovieSerializer(data=like_movies, many=True)
    print(netflix_serializer.is_valid(), disney_serializer.is_valid(), amazon_serializer.is_valid(), hulu_serializer.is_valid(), \
        popular_serializer.is_valid(), mvti_serializer.is_valid(), ) 
    # print(latest_serializer.is_valid() , highscore_serializer.is_valid() , like_serializer.is_valid())
    
    context={
        'netflix_movies' : netflix_serializer.data,
        'disney_movies' : disney_serializer.data,
        'amazon_movies' : amazon_serializer.data,
        'hulu_movies' : hulu_serializer.data,
        'popular_movies' : popular_serializer.data,
        'mvti_movies' : mvti_serializer.data,
        # 'latest_movies' : latest_serializer.data,
        # 'highscore_movies' : highscore_serializer.data,
    }
    return JsonResponse(context)



@api_view(['GET'])
def movie_detail(request, movie_pk) :
    # 상세페이지에서 보고 있는 영화
    movie = Movie.objects.get(pk=movie_pk)
    movie_list = [movie]
    serializer = MovieDetailSerializer(data = movie_list, many=True)

    # TMDB에서 제공하는 비슷한 콘텐츠
    movies = []
    url = f'https://api.themoviedb.org/3/movie/{movie.idx}/similar?api_key=1b7edbdee7b82ec37e80ba4d2b36db68&language=ko-KR&page=1'
    res = requests.get(url)
    similars = res.json().get('results')
    for similar in similars:
        temp_movie = Movie.objects.filter(title = similar['title'], released_date = similar['release_date']).first()
        if temp_movie != None:
            movies.append(temp_movie)

    # TMDB에서 제공하는 콘텐츠의 수
    movies_length = len(movies)
    add_count = 15 - movies_length
    # 15개 이상인 경우
    if add_count <= 0:
        movies = Movie.objects.order_by('-vote_cnt').distinct()[:15]
    # 15개 미만인 경우
    else:
        movie_genre = movie.movie_genre.all()
        movies_same_genre = Movie.objects.filter(movie_genre__id__in=movie_genre).order_by('-vote_cnt').distinct()[:add_count]
        movies += movies_same_genre
    similar_movies_serializer = MovieDetailSerializer(data = movies, many=True)
    print(serializer.is_valid(), similar_movies_serializer.is_valid())
    print(serializer)
    print(serializer.data)
    print(type(serializer.data))
    context = {
        "movie" : serializer.data, 
        "similar_movies" : similar_movies_serializer.data,
    }

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
    temp = {}
    print(winMovies)
    for winmovie in winMovies:
        otts = winmovie.movie_ott.all()
        for ott in otts:
            if ott in temp:
                temp[ott] += 1
            else:
                temp[ott] = 1
    if len(temp) == 0:
        most_ott = 'None',
    else:
        for tt in temp:
            most_ott = tt.name
            break
    print(most_ott)

    winMoviesSerializer = MovieSerializer(data = winMovies, many=True)
    # likeMoviesSerializer = MovieSerializer(data= likeMovies, many=True)

    print(winMoviesSerializer.is_valid())
    context = {
        'winMovies' : winMoviesSerializer.data,
        'ott' : most_ott, 
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
    print('시작')
    if not request.user.movie_comments.filter(pk=review_pk).exists():
        return Response({'detail': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
    
    
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == 'DELETE':
        review.delete()
        return Response({'id':review_pk}, status=status.HTTP_204_NO_CONTENT)