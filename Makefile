lint:
	poetry run flake8 project_1

install:
	poetry install

start:
	flask --app project_1.example --debug run

guni-start:
	poetry run gunicorn --workers=4 --bind=127.0.0.1:5000 project_1:app
