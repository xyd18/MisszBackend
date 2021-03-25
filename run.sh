cd missz
#python3 manage.py makemigrations dream
#python3 manage.py migrate
pip install -r ../requirements.txt
nohup python3 manage.py runserver 0.0.0.0:8000 > backend.log 2>&1 &