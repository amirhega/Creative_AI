"""Setup configurations."""
from setuptools import setup

setup(
    name='creative_ai',
    version='0.1.0',
    packages=['creative_ai'],
    include_package_data=True,
    install_requires=[
        'tqdm',
        'click',
        'tweepy',
        'spacy',
        'pronouncing'
    ]
)
