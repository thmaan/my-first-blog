from django.shortcuts import render
from django.utils import timezone
from .models import Post, Comment, PostLike, PostDeslike
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, CommentForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})
    
@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.views += 1
    post.save()
    likes_count = PostLike.objects.filter(post_id= pk, user= request.user).count()
    deslikes_count = PostDeslike.objects.filter(post_id = pk, user= request.user).count()
    if likes_count > 0:
        liked = True
    else:
        liked = False

    if deslikes_count > 0:
        desliked = True
    else:
        desliked = False 

    if liked or desliked:
        reacted = True
    else:
        reacted = False

    if reacted:    
        percent_likes = (likes_count / (likes_count + deslikes_count))* 100
        percent_deslikes = (deslikes_count / (likes_count + deslikes_count))* 100
    else:
        percent_deslikes = 0
        percent_likes = 0

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'liked': liked,
        'reacted': reacted,
        'percent_likes': percent_likes,
        'percent_deslikes': percent_deslikes}
        )
    
@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()

    return redirect('post_detail', pk=pk)
    
@login_required    
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

def post_like(request, pk):
    post_like, created = PostLike.objects.get_or_create(post_id=pk, user=request.user)
    return redirect('post_detail', pk=pk)

def post_deslike(request, pk):
    post_deslike, created = PostDeslike.objects.get_or_create(post_id=pk, user=request.user)
    return redirect('post_detail', pk=pk)

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)