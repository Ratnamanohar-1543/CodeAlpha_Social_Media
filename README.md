# CodeAlpha_SocialMedia (Task 2) - Instagram-style app
pip install -r requirements.txt
python manage.py makemigrations social
python manage.py migrate
python manage.py seed          # demo users (password demo1234) + 40 photo posts
python manage.py runserver
Log in as alex / demo1234, or register your own account and upload photos.
