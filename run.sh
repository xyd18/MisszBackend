cd missz
#python3 manage.py makemigrations dream
#python3 manage.py migrate
pip3 install -r ./requirements.txt
echo "finish install requirements.txt"
# nohup python3 missz/manage.py runserver 0.0.0.0:8000 > backend.log 2>&1 &
# echo "runserver"