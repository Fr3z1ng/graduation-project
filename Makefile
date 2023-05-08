PYTHON = python3
PIP = pip3

format:
	$(PYTHON) -m isort .
	$(PYTHON) -m black .

check:
	$(PYTHON) -m isort --check .
	$(PYTHON) -m black --check .

