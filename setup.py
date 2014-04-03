# -*- coding: utf-8 -*-
import sys
from setuptools import setup

setup(
    name='selenium-sunbro',
    version='0.01',
    author='Marcos Sánchez',
    author_email='arkanus@gmail.com',
    description="Easily create page objects with a declarative syntax",
    py_modules=['sunbro'],
    url='https://github.com/arkanus/selenium-sunbro',
    license='Mozilla Public License 2.0 (MPL 2.0)',
    keywords='selenium wedriver page object',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing',
        'Topic :: Utilities',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
    ],
    install_requires=['selenium']
)
