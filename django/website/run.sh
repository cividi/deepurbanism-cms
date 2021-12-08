export DJANGO_SETTINGS_MODULE=wagtail_vue.settings.dev
export PYTHONPATH=$PYTHONPATH:`pwd`/wagtail_vue/apps
export PYTHONPATH=$PYTHONPATH:`pwd`/wagtail_vue
django-admin makemigrations
django-admin migrate
django-admin runserver 0.0.0.0:8000
