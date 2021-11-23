from rest_framework import serializers
from .models import Recruit, Comment

class CommentSerializer(serializers.ModelSerializer):

    def getAuthorname(self, obj):
        return obj.author.username

    authorname = serializers.SerializerMethodField("getAuthorname")

    class Meta:
        model = Comment
        fields = ('id','content','authorname',)
        read_only_fields = ('recruit',)


class RecruitSerializer(serializers.ModelSerializer):
    comment_set = CommentSerializer(many=True, read_only=True) # read_only는 유효성검사에는 들어가지 않고 오직 읽을 때만 사용
    comment_count = serializers.IntegerField(
        source='comment_set.count', 
        read_only=True
    )
    def getAuthorname(self, obj):
        return obj.author.username
        
    authorname = serializers.SerializerMethodField("getAuthorname")

    class Meta:
        model = Recruit
        fields = ('id','title','authorname','ott_name','content', 'max_cnt', 'current_cnt', 'public_id', 'public_pw', 'comment_set', 'comment_count', 'created_at', 'updated_at')
        depth = 1
        

