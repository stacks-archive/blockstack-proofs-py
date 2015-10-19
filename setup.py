#!/usr/bin/python

from setuptools import setup, find_packages

setup(
    name='proofchecker',
    version='0.0.1',
    url='https://github.com/blockstack/proofchecker',
    license='GPLv3',
    author='Blockstack.org',
    author_email='support@blockstack.org',
    description='Python library for verifying proofs (twitter, github, domains etc) linked to a blockchain ID',
    keywords='blockchain bitcoin social proof verifications identity',
    packages=find_packages(),
    download_url='https://github.com/blockstack/proofchecker/archive/master.zip',
    zip_safe=False,
    install_requires=[
        'beautifulsoup4>=4.4.1',
        'pylibmc>=1.5.0',
        'requests>=2.8.1',
        'dnspython>=1.12.0'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet',
        'Topic :: Security :: Cryptography',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
