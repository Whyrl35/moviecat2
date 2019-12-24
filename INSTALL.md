# INSTALLATION

## How to quick install

```commandline
# cd /__your_path__/
# git clone __this_repository__
# cd __repository__
# virtualenv -p python3 venv
# source venv/bin/activate
# pip install -r requirements.txt
```

## How to test installation

```commandline
# FLASK_APP=run.py flask run
```

## What to do next ?

You need a WSGI server in front of the flask APP.\
You can either : 

* Install Apache2 + mode UWSGI
* Install nginx + gunicorn
