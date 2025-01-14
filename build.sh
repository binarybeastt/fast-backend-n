alembic upgrade head

# Start the app with Gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
