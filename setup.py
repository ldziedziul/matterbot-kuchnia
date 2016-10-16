# coding=utf-8
from distutils.core import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='matterbot-kuchnia',
    version='0.1',
    packages=[''],
    url='dziedziul.pl',
    license='MIT License',
    author='Łukasz Dziedziul',
    author_email='l.dziedziul at gmail',
    description='Tool for sending current lunch set from Kuchnia Domowa to the Mattermost',
    install_requires=requirements,
)
