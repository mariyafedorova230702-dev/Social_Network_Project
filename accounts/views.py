
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomUserChangeForm, PostForm, CommentForm
from .models import CustomUser, Post, Like, Follow, Comment
from django.shortcuts import get_object_or_404
from django.contrib import messages

@login_required(login_url='/login/')
def index(request):
    posts = Post.objects.select_related('author').prefetch_related('comments').order_by('-created_at')

    # Обработка нового поста
    if request.method == 'POST' and 'post_submit' in request.POST:
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('/')
    else:
        form = PostForm()

    # Форма для комментариев (каждому посту)
    comment_form = CommentForm()

    return render(request, 'accounts/index.html', {
        'posts': posts,
        'form': form,
        'comment_form': comment_form
    })


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            print(form.errors)
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'accounts/login.html', {
                'error': 'Неправильное имя пользователя или пароль'
            })

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('/')


@login_required(login_url='/login/')
def profile_view(request, username):
    try:
        profile_user = CustomUser.objects.get(username=username)
    except CustomUser.DoesNotExist:
        return render(request, '404.html', status=404)

    return render(request, 'accounts/profile.html', {
        'profile_user': profile_user
    })



@login_required(login_url='/login/')
def edit_profile_view(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(
            request.POST, request.FILES, instance=request.user
        )
        if form.is_valid():
            form.save()
            return redirect(f'/profile/{request.user.username}/')
    else:
        form = CustomUserChangeForm(instance=request.user)

    return render(request, 'accounts/edit_profile.html', {'form': form})


@login_required
def feed_view(request):
    following_users = Follow.objects.filter(follower=request.user).values_list('following', flat=True)

    posts = Post.objects.filter(author__in=following_users | [request.user]).order_by('-created_at')

    return render(request, 'feed.html', {'posts': posts})

@login_required
def follow_toggle(request, username):
    target = CustomUser.objects.get(username=username)


    follow, created = Follow.objects.get_or_create(
        follower=request.user,
        following=target
    )

    if not created:
        follow.delete()


    return redirect(f'/profile/{username}/')

@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    like, created = Like.objects.get_or_create(
        user=request.user,
        post=post
    )

    if not created:
        like.delete()

    return redirect('/')

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        parent_id = request.POST.get("parent_id")

        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post

            if parent_id:
                comment.parent = Comment.objects.filter(id=parent_id, post=post).first()

            comment.save()
        else:
            messages.error(request, "Комментарий не может быть пустым.")

    return redirect('index')

@login_required
def users_list(request):
    users = CustomUser.objects.all()
    return render(request, 'accounts/users.html', {'users': users})

