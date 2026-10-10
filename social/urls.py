from django.urls import path
from . import views as v
urlpatterns = [
    path("", v.feed, name="feed"), path("explore/", v.explore, name="explore"), path("new/", v.post_create, name="new"),
    path("p/<int:pk>/", v.post_detail, name="post"), path("like/<int:pk>/", v.like, name="like"),
    path("comment/<int:pk>/", v.comment, name="comment"), path("u/<str:username>/", v.profile, name="profile"),
    path("follow/<str:username>/", v.follow, name="follow"), path("edit/", v.edit_profile, name="edit")]
