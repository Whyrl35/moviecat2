# INSTALLATION

# API part

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


# FRONT part

You need to have npm or yarn installed on your system

## Quick install

```commandline
# cd /__your_path__/__repository__/www
# yarn install
# yarn build
```

## How to distribute ?

Simply make your previous configurer webserver (apache/nginx) point at the
`/__your_path__/__repository__/www/dist` directory
all compiled static filed are placed here by yarn/vue-cli