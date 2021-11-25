from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg, Prefetch

from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.http.response import JsonResponse

from .models import Recruit, Comment
from .serializers import CommentSerializer, RecruitSerializer
from accounts.models import User
import json
import requests
from django.contrib.auth import get_user_model


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JSONWebTokenAuthentication])
def index(request):
    if request.method == 'GET':
        recruits = get_list_or_404(Recruit.objects.order_by('-updated_at'))
        serializer = RecruitSerializer(data=recruits, many=True)
        print(serializer.is_valid())
        return Response(serializer.data)


@api_view(['GET','POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def create(request):
    if request.method == 'GET':
        serializer = RecruitSerializer(request.user.recruit_set, many=True)
        print(serializer.is_valid())
        return Response(serializer.data)

    elif request.method == 'POST':
        print('temp')
        serializer = RecruitSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def detail(request, recruit_pk):
    if request.method == 'GET':
        recruit = get_object_or_404(Recruit, pk=recruit_pk)
        serializer = RecruitSerializer(recruit)
        return Response(serializer.data)



@api_view(['GET','PUT'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def update(request, recruit_pk):
    recruit = get_object_or_404(Recruit, pk=recruit_pk)
    if not request.user.recruit_set.filter(pk=recruit_pk):
        print('123')
        return Response({'detail':'권한이 없습니다'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'PUT':
        serializer = RecruitSerializer(Recruit, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    elif request.method == 'GET':
        serializer = RecruitSerializer(recruit)
        return Response(serializer.data)


@api_view(['DELETE'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def delete(request, recruit_pk):
    recruit = get_object_or_404(Recruit, pk=recruit_pk)
    if not request.user.recruit_set.filter(pk=recruit_pk):
        return Response({'detail':'권한이 없습니다'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'DELETE':
        recruit.delete()
        return Response({'id':recruit_pk}, status=status.HTTP_204_NO_CONTENT)



@api_view(['POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def comment_create(request, recruit_pk):
    recruit = get_object_or_404(Recruit, pk=recruit_pk)
    print(request.data)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(author=request.user, recruit=recruit)
        print('12314')
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def comment_delete(request, recruit_pk, comment_pk):
    if not request.user.comment_set.filter(pk=comment_pk).exists():
        return Response({'detail': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
    
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.method == 'DELETE':
        comment.delete()
        return Response({'id':comment_pk}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JSONWebTokenAuthentication])
def pay(request, recruit_pk):
    if request.user.recruit_set.filter(pk=recruit_pk):
        return Response({'detail':'권한이 없습니다'}, status=status.HTTP_403_FORBIDDEN)

    url = "https://kapi.kakao.com"
    headers = {
        'Authorization': "KakaoAK " + "b76c688bcc686d6c8ef41ad79fca3b5e",
        'Content-type': 'application/x-www-form-urlencoded;charset=utf-8',
    }
    params = {
        'cid': "TC0ONETIME",
        'partner_order_id': '1001',
        'partner_user_id': 'jihwan',
        'item_name': '구독비',
        'quantity': 1,
        'total_amount': 3000,
        'vat_amount': 200,
        'tax_free_amount': 0,
        'approval_url': f'http://localhost:8080/{recruit_pk}/approval',
        'fail_url': 'http://localhost:8080/recruits/',
        'cancel_url': 'http://localhost:8080/recruits/',
    }
    response = requests.post(url+"/v1/payment/ready", params=params, headers=headers)
    response = json.loads(response.text)
    return Response(response)    


@api_view(['POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def approval(request, recruit_pk):
    recruit = get_object_or_404(Recruit, pk=recruit_pk)
    recruit.author.money += 3000
    recruit.author.save()
    print(recruit.author.username, recruit.author.money)
    recruit.current_cnt += 1
    recruit.user.add(request.user)
    recruit.save()
    
    recruit_serializer = RecruitSerializer(data=recruit)
    recruit_serializer.is_valid()
    context = {
        'id' : recruit.public_id,
        'pw' : recruit.public_pw,
        'money' : '3000',
        'ott' : recruit.ott_name,
    }
    return JsonResponse(context)


@api_view(['GET'])
def mypageRecruit(request, username) :
    person = get_object_or_404(get_user_model(), username=username)
    print(person)
    recruits = Recruit.objects.filter(user=person).distinct() # OneToMany 접근
    # likeMovies = Review.objects.filter(user=person).filter(liked=True).order_by('-created_at')
    # likeMovies = Movie.objects.filter(review__user=person).distinct()
    print(recruits)
    myRecruitSerializer = RecruitSerializer(data = recruits, many=True)
    # likeMoviesSerializer = MovieSerializer(data= likeMovies, many=True)

    print(myRecruitSerializer.is_valid())
    context = {
        'myRecruits' : myRecruitSerializer.data, 
    }
    return Response(context)