from setuptools import setup

setup(
    name='marvin',
    version='0.1',
    description='Marvin - Test Driven Development for RDF/OWL Ontologies',
    long_description='Marvin - Test Driven Development for RDF/OWL Ontologies',
    packages=['marvin'],
    author='Icaro Medeiros',
    author_email = 'icaro.medeiros@gmail.com',
    license = 'PSF',
    url = 'http://github.com/icaromedeiros/marvin',
    platforms = [ 'Python 2.6 and newer' ],

    install_requires=[
        "FuXi==1.4.production"
    ],
    dependency_links=[
        "https://pypi.python.org/pypi/FuXi/"
    ],
)
