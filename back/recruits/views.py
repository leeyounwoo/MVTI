from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from django.contrib.auth.decorators import login_required
from .models import Recruit, Comment
from .forms import RecruitForm, CommentForm
from django.db.models import Count, Avg, Prefetch
import requests
import json
from rest_framework.response import Response
from rest_framework.decorators import api_view
from accounts.models import User

# Create your views here.
@require_safe
def index(request):
    recruits = Recruit.objects.order_by('-updated_at')
    
    context = {
            'recruits': recruits,
    }
    return render(request, 'recruits/index.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def create(request):
    if request.method == 'POST':
        form =  RecruitForm(request.POST)
        if form.is_valid():
            recruit = form.save(commit=False)
            recruit.author = request.user
            recruit.save()
            return redirect('recruits:detail', recruit.pk)
    else:
        form = RecruitForm()
    context = {
        'form': form,
    }
    return render(request, 'recruits/create.html', context)


def detail(request, pk):
    queryset = Recruit.objects\
                .annotate(
                   
                )\
                .select_related('author')\
                .prefetch_related(
                    Prefetch(
                        'comment_set',
                        queryset=Comment.objects.select_related('author')
                    )
                )

    recruit = get_object_or_404(Recruit, pk=pk)
    
    form = CommentForm()
    context = {
        'recruit': recruit,
        'form': form,    
    }
    return render(request, 'recruits/detail.html', context)


@login_required
@require_POST
def delete(request, pk):
    recruit = get_object_or_404(Recruit, pk=pk)
    if request.user == recruit.author:
        recruit.delete()
    return redirect('recruits:index')


@login_required
@require_http_methods(['GET', 'POST'])
def update(request, pk):
    recruit = get_object_or_404(Recruit, pk=pk)
    if request.method == 'POST':
        form = RecruitForm(request.POST, instance=recruit)
        if form.is_valid():
            form.save()
            return redirect('recruits:detail', recruit.pk)
    else:
        form =  RecruitForm(instance=recruit)
    context = {
        'recruit': recruit,
        'form': form,
    }
    return render(request, 'recruits/update.html', context)

@require_POST
def create_comment(request, recruit_pk):
    if request.user.is_authenticated:
        recruit = get_object_or_404(Recruit, pk=recruit_pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.recruit = recruit
            comment.author = request.user
            comment.save()
        return redirect('recruits:detail', recruit.pk)


@login_required
@require_POST
def delete_comment(request, recruit_pk, comment_pk):
    review = get_object_or_404(Recruit, pk=recruit_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user == comment.author:
        comment.delete()
    return redirect('recruits:detail', review.pk)


@login_required
def pay(request, recruit_pk):
    user = get_object_or_404(User, pk=request.user.pk)
    recruit = get_object_or_404(Recruit, pk=recruit_pk)
    if recruit.author == user:
        return redirect('recruits:detail', recruit.pk)
    if request.method == "POST":
        URL = 'https://kapi.kakao.com/v1/payment/ready'
        headers = {
            "Authorization": "KakaoAK " + "b76c688bcc686d6c8ef41ad79fca3b5e",   # 변경불가
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",  # 변경불가
        }
        params = {
            "cid": "TC0ONETIME",    # 테스트용 코드
            "partner_order_id": "1001",     # 주문번호
            "partner_user_id": f"{user}",    # 유저 아이디
            "item_name": "구독 1달",        # 구매 물품 이름
            "quantity": "1",                # 구매 물품 수량
            "total_amount": "3000",        # 구매 물품 가격
            "tax_free_amount": "0",         # 구매 물품 비과세
            'approval_url': f'http://127.0.0.1:8000/community/{recruit_pk}/pay/approval/',
            'fail_url': f'http://127.0.0.1:8000/community/{recruit_pk}/pay/fail/',
            'cancel_url': f'http://127.0.0.1:8000/community/{recruit_pk}/pay/cancel/',
        }

        res = requests.post(URL, headers=headers, params=params)
        request.session['tid'] = res.json()['tid']      # 결제 승인시 사용할 tid를 세션에 저장
        next_url = res.json()['next_redirect_pc_url']   # 결제 페이지로 넘어갈 url을 저장
        print( request.session['tid'], next_url)
        return redirect(next_url)


    return render(request, 'recruits/pay.html')

@login_required
def approval(request, recruit_pk):
    user = get_object_or_404(User, pk=request.user.pk)
    URL = 'https://kapi.kakao.com/v1/payment/approve'
    headers = {
        "Authorization": "KakaoAK " + "b76c688bcc686d6c8ef41ad79fca3b5e",
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
    }
    params = {
        "cid": "TC0ONETIME",    # 테스트용 코드
        "tid": request.session['tid'],  # 결제 요청시 세션에 저장한 tid
        "partner_order_id": "1001",     # 주문번호
        "partner_user_id": f"{user}",    # 유저 아이디
        "pg_token": request.GET.get("pg_token"),     # 쿼리 스트링으로 받은 pg토큰
    }

    res = requests.post(URL, headers=headers, params=params)
    print(res.text)
    amount = res.json()['amount']['total']
    res = res.json()
    context = {
        'res': res,
        'amount': amount,
    }
    recruit = get_object_or_404(Recruit, pk=recruit_pk)
    recruit.author.money += amount
    recruit.author.save()
    print(recruit.author.username, recruit.author.money)
    recruit.current_cnt += 1
    recruit.save()
    return render(request, 'recruits/approval.html', context)


def fail(request, recruit_pk):
    return render(request, 'recruits/fail.html')


def cancel(request, recruit_pk):
    return render(request, 'recruits/cancel.html')
# @api_view(['POST'])
# def pay(request):
#     url = "https://kapi.kakao.com"
#     headers = {
#         'Authorization': "KakaoAK " + "b76c688bcc686d6c8ef41ad79fca3b5e",
#         'Content-type': 'application/x-www-form-urlencoded;charset=utf-8',
#     }
#     params = {
#         'cid': "TC0ONETIME",
#         'partner_order_id': '1001',
#         'partner_user_id': 'jihwan',
#         'item_name': '구독비',
#         'quantity': 1,
#         'total_amount': 0,
#         'vat_amount': 200,
#         'tax_free_amount': 0,
#         'approval_url': 'http://127.0.0.1:8000/community/',
#         'fail_url': 'http://127.0.0.1:8000/admin/',
#         'cancel_url': 'http://127.0.0.1:8000/community/1/',
#     }
#     response = requests.post(url+"/v1/payment/ready", params=params, headers=headers)
#     response = json.loads(response.text)
#     return Response(response)    