from rest_framework import serializers
from .models import Movie
from .models import Tournament


class MovieSerializer(serializers.ModelSerializer):
   
    class Meta : 
        model = Movie
        fields="__all__"


class TournamentSerializer(serializers.ModelSerializer): 
    class Meta : 
        model = Tournament
        fields = "__all__"