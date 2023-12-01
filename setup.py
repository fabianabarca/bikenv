from setuptools import setup, find_packages

VERSION = '0.1.1'
DESCRIPTION = 'Quantifies certain environmental factors that affect urban cycling'
LONG_DESCRIPTION = """
bikenv (biking environment) is intended to be used by researchers to quantify some environmental factors that affect urban cycling for a given region.
"""


setup(
    name='bikenv',
    packages=find_packages(include=['bikenv']),
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url='https://bikenv.readthedocs.io/en/latest/index.html',
    author='Fabián Abarca & Jose Daniel Marín & Derian Monge',
    license='MIT',
    install_requires=[
        'numpy==1.25.2',
        'scipy==1.11.2',
        'pandas==2.0.03',
        'geopandas==0.13.2',
        'osmnx==1.6.0',
        'networkx==3.1',
        'matplotlib==3.5.1',
        'scikit-learn==1.3.0',
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
    ],
    author_email="fabian.abarca@ucr.ac.cr",
)
