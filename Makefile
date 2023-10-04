.PHONY: all help clean line_code migrate migrate_app run pep8 qa flush

# target: all - Default target. Does nothing.
all:
	@clear
	@echo "Hello $(LOGNAME), nothing to do by default"
	@echo "Try 'make help'"

# target: help - Display callable targets.
help:
	@clear
	@egrep "^# target:" [Mm]akefile

# target: clean - Delete pycache
clean:
	echo "### Cleaning *.pyc and .DS_Store files "
	find . -name '*.pyc' -exec rm -f {} \;
	find . -name '.DS_Store' -exec rm -f {} \;
	find . -name "__pycache__" -type d -exec rm -rf {} +

# target: line_code - counting lines of code
line_code:
	echo "### Counting lines of code within the project"
	echo "# Python:" ; find . -name '*.py' -type f -exec cat {} + | wc -l
	echo "# JavaScript:" ; find . -name '*.js' -type f -exec cat {} + | wc -l
	echo "# HTML:" ; find . -name '*.html' -type f -exec cat {} + | wc -l
	echo "# CSS:" ; find . -name '*.css' -type f -exec cat {} + | wc -l

env_gen:
	cp example.env .env
# target: migrate - Makemigrations and migration
migrate:
	python3 manage.py makemigrations && python3 manage.py migrate

# target: migrate - Makemigrations application and migration
migrate_app:
	python3 manage.py makemigrations $(APP) && python3 manage.py migrate

# target: run - Run server
run:
	python3 manage.py runserver 0.0.0.0:8000

# target: mypy - Run static typing
mypy:
	mypy --config-file=mypy.ini picasso

# target: pylint - Checks for errors, enforces a coding standard, looks for code smells.
pylint:
	pylint picasso

# target: pep8 - Run code style test
pep8:
	flake8 --count

# target: isort - Sorts imports
isort:
	isort picasso

# target: black - Code formatting
fmt_check:
	black picasso

# target: all in one linters
lint: mypy pylint pep8

# target: all in one formatters
fmt: isort fmt_check

# target: qa - Run tests
qa:
	pytest

# target: flush - clean database
flush:
	python3 manage.py flush

# target: worker - Run celery worker with auto reload
worker:
	watchmedo auto-restart --directory=./ --pattern=\*.py --recursive --  celery -A picasso worker -l INFO --autoscale=10,2 --purge
