.PHONY: install gendiff package-install lint tests test-coverage

install:
	poetry install

gendif:
	poetry run gendiff -h

package-install:
	python3.10 -m pip install --user dist/*.whl

lint:
	poetry run flake8 gendiff

tests:
	poetry run pytest

test-coverage:
	poetry run pytest --cov=gendiff/scripts --cov-report xml