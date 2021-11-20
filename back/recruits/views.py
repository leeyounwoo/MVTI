from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from django.contrib.auth.decorators import login_required
from .models import Recruit, Comment
from .forms import RecruitForm, CommentForm
from django.db.models import Count, Avg, Prefetch

# Create your views here.
@require_safe
def index(request):
    recruits = Recruit.objects.order_by('-updated_at')
    
    context = {
            'recruits': recruits,
    }
    return render(request, 'community/index.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def create(request):
    if request.method == 'POST':
        form =  RecruitForm(request.POST)
        if form.is_valid():
            recruit = form.save(commit=False)
            recruit.author = request.user
            recruit.save()
            return redirect('community:detail', recruit.pk)
    else:
        form = RecruitForm()
    context = {
        'form': form,
    }
    return render(request, 'community/create.html', context)


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
    return render(request, 'community/detail.html', context)


@login_required
@require_POST
def delete(request, pk):
    recruit = get_object_or_404(Recruit, pk=pk)
    if request.user == recruit.author:
        recruit.delete()
    return redirect('community:index')


@login_required
@require_http_methods(['GET', 'POST'])
def update(request, pk):
    recruit = get_object_or_404(Recruit, pk=pk)
    if request.method == 'POST':
        form = RecruitForm(request.POST, instance=recruit)
        if form.is_valid():
            form.save()
            return redirect('community:detail', recruit.pk)
    else:
        form =  RecruitForm(instance=recruit)
    context = {
        'recruit': recruit,
        'form': form,
    }
    return render(request, 'community/update.html', context)

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
        return redirect('community:detail', recruit.pk)


@login_required
@require_POST
def delete_comment(request, recruit_pk, comment_pk):
    review = get_object_or_404(Recruit, pk=recruit_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user == comment.author:
        comment.delete()
    return redirect('community:detail', review.pk)