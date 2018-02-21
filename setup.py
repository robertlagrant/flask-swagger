"""
Flask-Swagger
-------------

This is the description for that library
"""
from setuptools import setup


setup(
    name='Flask-Swagger',
    version='0.1',
    url='http://example.com/flask-swagger/',
    license='BSD',
    author='Robert Grant',
    author_email='robertlagrant@gmail.com',
    description='A Flask extension to enable quick API creation from a Swagger file',
    long_description=__doc__,
    py_modules=['flask_swagger'],
    # if you would be using a package instead use packages instead
    # of py_modules:
    # packages=['flask_sqlite3'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask', 'swagger_parser'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
