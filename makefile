.PHONY: install test smoke login functional clean setup

install:
	pip install -r requirements.txt

setup: install
	mkdir -p downloads
	mkdir -p screenshots

test:
	pytest tests/ -v

smoke:
	pytest -m smoke -v

login:
	pytest -m login -v

functional:
	pytest -m functional -v

content-template:
	pytest -m content_template -v

section:
	pytest -m section -v

download:
	pytest -m download -v

dashboard:
	pytest -m dashboard -v

parallel:
	pytest -n 4 tests/

html-report:
	pytest --html=report.html --self-contained-html tests/

clean:
	find . -type d -name "__pycache__" -delete
	find . -name "*.pyc" -delete
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -f .coverage
	rm -f *.png
	rm -f report.html
