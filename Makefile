lint:
	poetry run flake8 project_1

install:
	poetry install

start:
	flask --app project_1.lesson.example --debug run