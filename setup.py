from setuptools import setup, find_packages

setup(
    name='openletters',
    version='0.1',
    description='',
    author='Open Knowledge Foundation (Open Literature WG)',
    author_email='info@okfn.org',
    url='http://knowledgeforge.net/project/letters/',
    install_requires=[
        # please use pip-requirements.txt
        "Pylons>=0.9.7",
        "SQLAlchemy>=0.5",
        "Genshi>=0.4",
    ],
    setup_requires=["PasteScript>=1.6.3"],
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
    """,
)
