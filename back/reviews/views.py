from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from django.contrib.auth.decorators import login_required
from .models import Review, ReviewComment
from .forms import ReviewForm, ReviewCommentForm
from django.db.models import Count, Avg, Prefetch
import requests
import json
from rest_framework.response import Response
from movies.models import Movie
from accounts.models import User

# Create your views here.
@require_safe
def index(request):
    reviews = Review.objects.order_by('-updated_at')
    
    context = {
            'reviews': reviews,
    }
    return render(request, 'reviews/index.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def create(request, movie_pk):
    if request.method == 'POST':
        form =  ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.save()
            return redirect('reviews:detail', review.pk)
    else:
        form = ReviewForm()
    movie = Movie.objects.get(pk=movie_pk)
    print(movie)
    context = {
        'form': form,
        'movie': movie,
    }
    return render(request, 'reviews/create.html', context)


def detail(request, pk):
    queryset = Review.objects\
                .annotate(
                   
                )\
                .select_related('author')\
                .prefetch_related(
                    Prefetch(
                        'comment_set',
                        queryset=ReviewComment.objects.select_related('author')
                    )
                )

    review = get_object_or_404(Review, pk=pk)
    movie  = Movie.objects.get(title = review.review_movie)
    form = ReviewCommentForm()
    context = {
        'review': review,
        'form': form,
        'movie' : movie,    
    }
    return render(request, 'reviews/detail.html', context)


@login_required
@require_POST
def delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.user == review.author:
        review.delete()
    return redirect('reviews:index')


@login_required
@require_http_methods(['GET', 'POST'])
def update(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('reviews:detail', review.pk)
    else:
        form =  ReviewForm(instance=review)
    context = {
        'review': review,
        'form': form,
    }
    return render(request, 'reviews/update.html', context)

@require_POST
def create_comment(request, review_pk):
    if request.user.is_authenticated:
        review = get_object_or_404(Review, pk=review_pk)
        form = ReviewCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.review = review
            comment.author = request.user
            comment.save()
        return redirect('reviews:detail', review.pk)


@login_required
@require_POST
def delete_comment(request, review_pk, comment_pk):
    review = get_object_or_404(Review, pk=review_pk)
    comment = get_object_or_404(ReviewComment, pk=comment_pk)
    if request.user == comment.author:
        comment.delete()
    return redirect('reviews:detail', review.pk)