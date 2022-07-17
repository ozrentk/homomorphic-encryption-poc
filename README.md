# REPO: homomorphic-encryption-poc

POC for homomorphic encryption REST app

## Startup

- created Github project

## Venv

```
python3 -m venv venv
source ../venv/bin/activate
```

## Git

```
git -C src clone https://github.com/ozrentk/homomorphic-encryption-poc
```

Now you can open repo locally in your favorite Git client.

## Python: PIP

```
pip install flask
pip install flask_restful

pip freeze > requirements.txt
```

## Python: flask

```
python api.py
```

## Heroku

```
heroku login
heroku container:login

heroku create he-poc
heroku container:push web --app he-poc

heroku open --app he-poc
```

Add Procfile and you're good to go

```
gunicorn --bind 0.0.0.0:5007 api:app
```