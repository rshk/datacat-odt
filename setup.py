##------------------------------------------------------------
## OpenData Trentino plugin for DataCat
##------------------------------------------------------------

import sys

from setuptools import setup, find_packages


version = '0.1-alpha'

install_requires = [
    'datacat',
]

dependency_links = [
    'git+https://github.com/rshk/datacat@master#egg=datacat-dev',
]

# if sys.version_info < (2, 7):
#     install_requires.append('argparse')

## Tests should use the common test cases from datacat,
## although I think we'll need mocks for most of them..
tests_require = [
    'pytest',
    'pytest-pep8',
    'pytest-cov',
]

entry_points = {
    'datacat.plugins.readers': [
        'pat_geocatalogo = datacat_odt:PatGeocatalogoReader',
        'pat_statistica = datacat_odt:PatStatisticaReader',
        'pat_statistica_subpro = datacat_odt:PatStatisticaSubproReader',
        'tn_entilocali = datacat_odt:TrentoEntiLocaliReader',
    ],
}

extra = {}
if sys.version_info >= (3,):
    extra['use_2to3'] = True


setup(
    name='datacat_odt',
    version=version,
    packages=find_packages(),
    url='http://rshk.github.io/datacat-odt',
    license='3-Clause BSD License',
    author='Samuele Santi',
    author_email='samuele@samuelesanti.com',
    description='datacat plugin for the OpenData Trentino Project',
    long_description='datacat plugin for the OpenData Trentino Project',
    install_requires=install_requires,
    dependency_links=dependency_links,
    tests_require=tests_require,
    test_suite='datapub_odt.tests',
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 2.7",
    ],
    package_data={'': ['README.rst', 'LICENSE']},
    entry_points=entry_points,
    **extra)
