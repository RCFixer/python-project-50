.PHONY: install gendiff package-install

install:
	poetry install

gendif:
	poetry run gendiff -h

package-install:
	python3.10 -m pip install --user dist/*.whl