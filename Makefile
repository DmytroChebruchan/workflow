reformatting:
	isort .
	black .
	autoflake .
	make lint

lint:
	flake8 .
	mypy .

