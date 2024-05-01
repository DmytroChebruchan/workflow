reformatting:
	isort .
	black .
	make lint

lint:
	flake8 .
	mypy .

