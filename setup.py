import io
import os
import re

from setuptools import find_packages
from setuptools import setup


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding='utf-8') as fd:
        return re.sub(text_type(r':[a-z]+:`~?(.*?)`'), text_type(r'``\1``'), fd.read())


setup(
    name="inferiot",
    version="1.0.1",
    url="https://github.com/prafulmaka/inferiot",
    license='MIT',

    author="Praful Maka, Mohammad Sameer Beig, Daniel Gallagher, John Groboske, Otu Ekanem",
    author_email="praful.maka@gmail.com",

    description="Python facade for connecting to Smarthub's Infer IOT center",
    long_description=read("README.rst"),

    packages=find_packages(exclude=('tests',)),

    install_requires=['pandas'],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
