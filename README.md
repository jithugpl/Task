Instructions to Run the E-Commerce Application
git clone <repository_url>
in bash:
cd <project_folder>
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

