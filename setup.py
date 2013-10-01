from setuptools import setup, find_packages

__long_description__ = '''A project which explores the correspondence and social networks of the
nineteenth century literary world. Currently the project focuses on Charles
Dickens but this will be expanded as new datasets are created.'''
__version__ = '0.1'
__description__ = __long_description__.split('.')[0]
__license__ = 'AGPL'

setup(
    name='openletters',
    version=__version__,
    license=__license__,
    description=__description__,
    long_description=__long_description__,
    author='Open Knowledge Foundation (Open Literature WG)',
    author_email='info@okfn.org',
    # set requirements.txt
    install_requires=[
    ],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    test_suite='nose.collector',
    package_data={'openletters': ['i18n/*/LC_MESSAGES/*.mo']},
    #message_extractors={'openletters': [
    #        ('**.py', 'python', None),
    #        ('public/**', 'ignore', None)]},
    zip_safe=False,
)
