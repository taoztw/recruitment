
export DJANGO_SETTINGS_MODULE=settings.local

nohup uvicorn recruitment.asgi:application --port 8001 --workers 2 &
nohup uvicorn recruitment.asgi:application --port 8002 --workers 2 &
