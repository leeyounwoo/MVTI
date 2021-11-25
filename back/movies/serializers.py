from django.db.models import manager
from rest_framework import serializers
from .models import Movie, Tournament, Genre, Review, Ott


class GenreSerializer(serializers.ModelSerializer):

    class Meta : 
        model = Genre
        fields = "__all__"


class MovieSerializer(serializers.ModelSerializer):
   
    class Meta : 
        model = Movie
        fields="__all__"

class OttSerializer(serializers.ModelSerializer):
   
    class Meta : 
        model = Ott
        fields="__all__"


class TournamentSerializer(serializers.ModelSerializer): 
    class Meta : 
        model = Tournament
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Review
        fields = ('id','content', 'rating', 'user',)
        read_only_fields = ('user',)


class MovieDetailSerializer(serializers.ModelSerializer): # 영화상세
    genres = GenreSerializer(many=True, read_only=True)
    review_set = ReviewSerializer(many=True, read_only=True)

    class Meta : 
        model = Movie
        fields = "__all__"

