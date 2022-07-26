rm -rf *.sqlite3
rm -rf */migrations/00*.py
python manage.py makemigrations
python manage.py migrate

