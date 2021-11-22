import requests
import json

idx = 1
ret = []
for page in range(1, 2):
    url = "https://api.themoviedb.org/3/movie/popular?api_key=1b7edbdee7b82ec37e80ba4d2b36db68&language=ko-KR&page=" + str(page)
    res = requests.get(url)
    first = res.json().get('results')
    print(len(first))