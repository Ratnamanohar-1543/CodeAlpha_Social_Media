import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from social.models import Post, Comment, Like, Follow
NAMES = ["alex", "mia", "ravi", "sana", "john", "priya", "kiran", "lily"]
CAPS = ["Golden hour vibes ✨", "Weekend escape 🌿", "Coffee first ☕", "Chasing sunsets 🌅", "Good times, good people", "Lost in the city 🏙", "Simple moments", "Nature never disappoints 🌲"]
class Command(BaseCommand):
    def handle(self, *a, **k):
        random.seed(3); users = []
        for n in NAMES:
            u, c = User.objects.get_or_create(username=n)
            if c: u.set_password("demo1234"); u.save(); u.profile.bio = f"Hi, I'm {n.title()} 📸 Sharing life one photo at a time"; u.profile.save()
            users.append(u)
        i = 0
        for u in users:
            for _ in range(5):
                i += 1
                Post.objects.get_or_create(author=u, image_url=f"https://picsum.photos/seed/snap{i}/800/800", defaults={"caption": random.choice(CAPS)})
        posts = list(Post.objects.all())
        for u in users:
            for o in random.sample(users, 4):
                if o != u: Follow.objects.get_or_create(follower=u, followed=o)
            for p in random.sample(posts, 15): Like.objects.get_or_create(user=u, post=p)
            for p in random.sample(posts, 5): Comment.objects.create(post=p, author=u, text=random.choice(["Love this! 😍", "Stunning 🔥", "Amazing shot!", "Goals 🙌"]))
        self.stdout.write("Seeded demo users (password: demo1234) and 40 posts")
