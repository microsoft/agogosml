.PHONY: clean clean-test clean-pyc clean-build docs help
.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys

try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . \( -path ./env -o -path ./venv -o -path ./.env -o -path ./.venv \) -prune -o -name '*.egg-info' -exec rm -fr {} +
	find . \( -path ./env -o -path ./venv -o -path ./.env -o -path ./.venv \) -prune -o -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

lint: ## check python style
	flake8 cli tests
	pylint cli
	bandit -c .banditrc -r cli
	isort --check-only --recursive cli

test:
	## Fail fast in CI, maxfail=1
	py.test --maxfail=1 --cov=cli --cov-report term-missing \
		--cov-report xml:tests_cov_output/coverage.xml \
		--cov-report html:tests_cov_output/htmlcov \
		--cov-fail-under=70 \
		--junitxml=tests_cov_output/TEST-cli.xml

test-dev:
	py.test --cov=cli --cov-report term-missing \
		--cov-report html:tests_cov_output/htmlcov
	$(BROWSER) ./tests_cov_output/htmlcov/index.html


# for tox - see https://github.com/pyenv/pyenv-virtualenv/issues/202   for setup of pyenv and tox py versions
# see https://github.com/samstav/circleci-python-sandbox/issues/1

test-all: ## run tests on every Python version with tox
	tox

test-single: ## run tests on specific Python version with tox
	echo "using tox and buidling $$TOX_VERSION"
	tox -e ${TOX_VERSION}

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/cli.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ cli
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

servedocs: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

release: dist ## package and upload a release
	twine upload dist/*

dist: clean ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: clean ## install the package to the active Python's site-packages
	python setup.py install

installedit: clean ## install the package while dynamically picking up changes to source files
	pip install --editable .

dockerbuild: clean
	echo "tox version set to ${TOX_VERSION}"
	@if [ "${TOX_VERSION}" ]; then \
		echo "buidling $$TOX_VERSION"; \
		docker build -t agogosml_cli --no-cache --build-arg TOX_VERSION=${TOX_VERSION} . ; \
	else \
		echo "buidling py37"; \
		docker build -t agogosml_cli --no-cache . ; \
	fi
