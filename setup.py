from setuptools import setup

setup(
    name='diderot',
    version='0.1',
    description='Diderot - Test Driven Development for RDF/OWL Ontologies',
    long_description='Diderot - Test Driven Development for RDF/OWL Ontologies',
    packages=['diderot'],
    package_data = {
        'rules': ['*.n3']
    },
    author='Icaro Medeiros',
    author_email = 'icaro.medeiros@gmail.com',
    license = 'PSF',
    url = 'http://github.com/icaromedeiros/diderot',
    platforms = [ 'Python 2.6 and newer' ],
    install_requires=[
        "FuXi==1.4.1.production", "sure==1.2.2"
    ]
)
