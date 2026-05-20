**Installation Guide**
Clone the Repository
cd SRM

**Create a Virtual Environment**
python -m venv venv

**Activate the Virtual Environment**
Windows
venv\Scripts\activate
Linux / macOS
source venv/bin/activate

**Install Dependencies**
pip install django


** Apply Migrations**
python manage.py migrate

**Run the Development Server**
python manage.py runserver

The application will be available at:

http://127.0.0.1:8000/
