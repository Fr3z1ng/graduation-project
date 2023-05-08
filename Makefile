PYTHON = python3
PIP = pip3

format:
	$(PYTHON) -m black .
	$(PYTHON) -m isort .

check:
	$(PYTHON) -m isort --check .
	$(PYTHON) -m black --check .
	$(PYTHON) -m flake8 --exclude=venv --show-source --statistics

