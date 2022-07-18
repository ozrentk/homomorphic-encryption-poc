# REPO: homomorphic-encryption-poc

POC for homomorphic encryption REST app

## Startup

- created Github project

## Venv

```
python3 -m venv venv
. ../venv/bin/activate
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

Add Procfile and then deploy.
```
web: gunicorn --bind 0.0.0.0:$PORT api:app
```

When you deploy, scale your web.
```
heroku ps:scale web=1
```

Now check the result, should be god to go.

Oh, btw, logs:
```
heroku logs --tail
```

Cheers!