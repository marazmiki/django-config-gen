clean:
	rm -rf django_config_gen.egg-info
	rm -rf htmlcov
	find . -name "*.pyc" -exec rm -rf {} \;
test:
	python setup.py test

release:
	python setup.py sdist --format=zip,bztar,gztar register upload

flake8:
	flake8 --ignore=E501 setup.py tests.py
	flake8 --ignore=E501 --max-complexity 12 django_config_gen

coverage:
	coverage run --include=django_config_gen/* setup.py test
	coverage html
