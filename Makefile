CWD="`pwd`"

clean:
	@find . -name "*.pyc" -delete
	@find . -name "__pycache__" -delete

test: clean pep8 pep8_tests
	@echo "Running pep8, unit and integration tests..."
	@coverage erase
	@nosetests -s --with-coverage --cover-branches --cover-inclusive --cover-package=diderot --tests=tests --with-xunit --with-spec --spec-color
	@coverage report

unit: clean
	@echo "Running unit tests..."
	@nosetests -s --with-coverage --cover-branches --cover-inclusive --cover-package=diderot --tests=tests/unit --with-xunit --with-spec --spec-color

functional: clean
	@echo "Running functional tests..."
	@nosetests -s --with-coverage --cover-branches --cover-inclusive --cover-package=diderot --tests=tests/functional --with-xunit --with-spec --spec-color

acceptance: clean
	@echo "Running acceptance tests..."
	@nosetests -s --tests=example/test --with-xunit --with-spec --spec-color

pep8:
	@echo "Checking source-code PEP8 compliance"
	@-pep8 diderot --ignore=E501,E126,E127,E128

pep8_tests:
	@echo "Checking tests code PEP8 compliance"
	@-pep8 tests --ignore=E501,E126,E127,E128

install:
	@echo "Installing dependencies..."
	@pip install ez_setup
	@pip install -r requirements.txt
	@pip install -r requirements_test.txt

report:
	@echo "Making report..."
	@cd $(CWD)/project_report; pdflatex report.tex
	@cd $(CWD)/project_report; bibtex report.aux
	@cd $(CWD)/project_report; pdflatex report.tex
	@cd $(CWD)/project_report; bibtex report.aux
	@cd $(CWD)/project_report; pdflatex report.tex
	@cd $(CWD)/project_report; open report.pdf
