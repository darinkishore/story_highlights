release: python manage.py collectstatic --noinput
web: gunicorn vercel_app.wsgi:app
