from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
class Profile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    bio = models.CharField(max_length=150, blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True)
    @property
    def pic(self):
        return self.avatar.url if self.avatar else f"https://picsum.photos/seed/avatar-{self.user.username}/150"
@receiver(post_save, sender=User)
def make_profile(sender, instance, created, **kw):
    if created: Profile.objects.create(user=instance)
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="posts/", blank=True)
    image_url = models.URLField(blank=True)
    caption = models.CharField(max_length=300, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    @property
    def src(self): return self.image.url if self.image else self.image_url
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="likes", on_delete=models.CASCADE)
    class Meta: unique_together = ("user", "post")
class Follow(models.Model):
    follower = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)
    class Meta: unique_together = ("follower", "followed")
