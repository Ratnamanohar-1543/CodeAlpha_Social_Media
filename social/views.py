from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Comment, Like, Follow

def register(r):
    form = UserCreationForm(r.POST or None)
    if form.is_valid():
        login(r, form.save()); return redirect("feed")
    return render(r, "registration/register.html", {"form": form})

def _ctx(r, posts, **extra):
    posts = posts.select_related("author__profile").prefetch_related("comments__author", "likes")
    liked = set(Like.objects.filter(user=r.user).values_list("post_id", flat=True))
    return {"posts": posts, "liked": liked, **extra}

@login_required
def feed(r):
    ids = list(r.user.following.values_list("followed_id", flat=True)) + [r.user.id]
    stories = User.objects.filter(id__in=ids).select_related("profile")
    suggest = User.objects.exclude(id__in=ids).select_related("profile")[:5]
    return render(r, "social/feed.html", _ctx(r, Post.objects.filter(author_id__in=ids).order_by("-created"), stories=stories, suggest=suggest))

@login_required
def explore(r):
    q = r.GET.get("q", "")
    users = User.objects.filter(username__icontains=q).select_related("profile")[:10] if q else []
    return render(r, "social/explore.html", {"posts": Post.objects.order_by("-created"), "users": users, "q": q})

@login_required
def post_create(r):
    if r.method == "POST" and r.FILES.get("image"):
        Post.objects.create(author=r.user, image=r.FILES["image"], caption=r.POST.get("caption", ""))
        return redirect("profile", username=r.user.username)
    return render(r, "social/new.html")

@login_required
def post_detail(r, pk):
    return render(r, "social/post.html", _ctx(r, Post.objects.filter(pk=pk)))

@login_required
def like(r, pk):
    obj, created = Like.objects.get_or_create(user=r.user, post_id=pk)
    if not created: obj.delete()
    return JsonResponse({"liked": created, "count": Like.objects.filter(post_id=pk).count()})

@login_required
def comment(r, pk):
    if r.method == "POST" and r.POST.get("text", "").strip():
        Comment.objects.create(post_id=pk, author=r.user, text=r.POST["text"])
    return redirect(r.META.get("HTTP_REFERER") or "feed")

@login_required
def profile(r, username):
    u = get_object_or_404(User, username=username)
    return render(r, "social/profile.html", {"u": u, "posts": u.post_set.order_by("-created"),
        "is_following": Follow.objects.filter(follower=r.user, followed=u).exists()})

@login_required
def follow(r, username):
    u = get_object_or_404(User, username=username)
    if u != r.user:
        obj, created = Follow.objects.get_or_create(follower=r.user, followed=u)
        if not created: obj.delete()
    return redirect(r.META.get("HTTP_REFERER") or "feed")

@login_required
def edit_profile(r):
    p = r.user.profile
    if r.method == "POST":
        p.bio = r.POST.get("bio", "")
        if r.FILES.get("avatar"): p.avatar = r.FILES["avatar"]
        p.save(); return redirect("profile", username=r.user.username)
    return render(r, "social/edit.html", {"p": p})
