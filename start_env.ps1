cd "C:\Users\Arpit\PycharmProjects\pythonProject"
.\venv\Scripts\activate
$env:FLASK_APP = "arpit_restaurantAPP.py"
$env:FLASK_DEBUG = "1"
$env:PYTHONDONTWRITEBYTECODE = "1"
flask run
