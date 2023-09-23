## Installations
pip install django

## DB Migration
python manage.py makemigrations 
python manage.py migrate
python manage.py loaddata seed.json

# Run server
python manage.py runserver

# Formating

pip install autopep8
python -m autopep8 --in-place */**/*.py