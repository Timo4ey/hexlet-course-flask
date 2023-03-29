lint:
	poetry run flake8 project_1

install:
	poetry install

start:
	poetry run flask --app project_1:app run

PORT ?= 8000
guni-start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) project_1:app
