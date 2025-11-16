release: python manage.py migrate --noinput || true
web: python manage.py collectstatic --noinput && python -m gunicorn liftandlight.wsgi --bind 0.0.0.0:$PORT --log-file -

