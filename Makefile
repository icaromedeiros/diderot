clean:
	@find . -name "*.pyc" -delete
	@find . -name "__pycache__" -delete

test: clean pep8 pep8_tests
	@echo "Running pep8, unit and integration tests..."
	@nosetests -s  --with-coverage --cover-inclusive --cover-package=marvin --tests=tests --with-xunit

unit: clean
	@echo "Running unit tests..."
	@nosetests -s --with-coverage --cover-inclusive --cover-package=marvin --tests=tests/unit --with-xunit

functional: clean
	@echo "Running functional tests..."
	@nosetests -s --with-coverage --cover-inclusive --cover-package=marvin --tests=tests/functional --with-xunit

acceptance: clean
	@echo "Running acceptance tests..."
	@nosetests -s --with-coverage --cover-inclusive --cover-package=marvin --tests=tests/acceptance --with-xunit

pep8:
	@echo "Checking source-code PEP8 compliance"
	@-pep8 marvin --ignore=E501,E126,E127,E128

pep8_tests:
	@echo "Checking tests code PEP8 compliance"
	@-pep8 tests --ignore=E501,E126,E127,E128

install:
	@echo "Installing dependencies..."
	@pip install ez_setup
	@pip install -r requirements.txt
	@pip install -r requirements_test.txt
