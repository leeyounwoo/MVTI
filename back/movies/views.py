from django.shortcuts import render, redirect
import requests
import json
from .models import Movie
# Create your views here.

def add_info(request):
    for page in range(1, 200):
        url = "https://api.themoviedb.org/3/movie/popular?api_key=1b7edbdee7b82ec37e80ba4d2b36db68&language=ko-KR&page=" + str(page)
        res = requests.get(url)
        infos = res.json().get('results')
        for i in range(len(infos)):
            if not infos[i]["poster_path"] or not infos[i]['title'] or not infos[i]['overview'] or not infos[i]['release_date'] or not infos[i]['vote_count'] or not infos[i]['genre_ids']:
                continue

            print( infos[i]['title'],
                infos[i]['overview'],
                infos[i]['release_date'],
                infos[i]['poster_path'])
            print(infos[i]['popularity'],
                infos[i]['vote_average'],
                infos[i]['vote_count'])
            
            Movie(
                title = infos[i]['title'],
                overview = infos[i]['overview'],
                released_date = infos[i]['release_date'],
                poster_path = infos[i]['poster_path'],
                popularity = infos[i]['popularity'],
                vote_average = infos[i]['vote_average'],
                vote_cnt = infos[i]['vote_count'],
            ).save()
    return redirect('community:index')