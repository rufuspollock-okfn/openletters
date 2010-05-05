from setuptools import setup, find_packages
import sys
sys.path.insert(0, '.')
from openletters import __version__, __description__, __license__
from openletters import __doc__ as __long_description__

setup(
    name='openletters',
    version=__version__,
    license=__license__,
    description=__description__,
    long_description=__long_description__,
    author='Open Knowledge Foundation (Open Literature WG)',
    author_email='info@okfn.org',
    url='http://knowledgeforge.net/project/letters/',
    install_requires=[
        # please use pip-requirements.txt
        # "Pylons>=0.9.7",
        # "SQLAlchemy>=0.5",
        # "Genshi>=0.4",
        # ...
    ],
    # setup_requires=["PasteScript>=1.6.3"],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    test_suite='nose.collector',
    package_data={'openletters': ['i18n/*/LC_MESSAGES/*.mo']},
    #message_extractors={'openletters': [
    #        ('**.py', 'python', None),
    #        ('public/**', 'ignore', None)]},
    zip_safe=False,
    paster_plugins=['PasteScript', 'Pylons'],
    entry_points="""
    [paste.app_factory]
    main = openletters.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller

    [paste.paster_command]
    db = openletters.cli:ManageDb
    load = openletters.cli:Load
    fixtures = openletters.cli:Fixtures
    """,
)
