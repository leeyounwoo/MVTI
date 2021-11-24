from rest_framework import serializers
from .models import Movie, Tournament, Genre, Review


class GenreSerializer(serializers.ModelSerializer):

    class Meta : 
        model = Genre
        fields = "__all__"


class MovieSerializer(serializers.ModelSerializer):
   
    class Meta : 
        model = Movie
        fields="__all__"


class TournamentSerializer(serializers.ModelSerializer): 
    class Meta : 
        model = Tournament
        fields = "__all__"


class MovieDetailSerializer(serializers.ModelSerializer): # 영화상세
    genres = GenreSerializer(many=True, read_only=True)

    class Meta : 
        model = Movie
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Review
        fields = ('id','content', 'rating', 'user',)
        read_only_fields = ('user',)