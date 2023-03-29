lint:
	poetry run flake8 project_1

install:
	poetry install

start:
	flask --app project_1.example --debug run

guni-start:
	poetry run gunicorn --workers=4 --bind=0.0.0.0:3000 project_1:app
