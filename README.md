# Auto Parts Parser
This Django application allows you to collect information about automotive parts from Advance Auto Parts based on the specified category, year, type, brand, model, and engine. It uses Selenium to automate getting job details and storing them in a database.
## Installation

```shell
git clone https://github.com/Ilyakson/CarParser.git
python -m venv venv
venv\Scripts\activate (on Windows)
source venv/bin/activate (on macOS)
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
