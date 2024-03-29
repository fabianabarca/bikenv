from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Quantifies certain environmental factors that affect cycling'
LONG_DESCRIPTION = """
bikenv (biking environment) is intended to be used by researchers to quantify some environmental factors that affect cycling for a given region.
"""


setup(
    name='bikenv',
    packages=find_packages(include=['bikenv']),
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url='https://bikenv.readthedocs.io/en/latest/index.html',
    author='Fabián Abarca & Jose Daniel Marín',
    license='MIT',
    install_requires=[
        'numpy',
        'scipy',
        'pandas',
        'geopandas',
        'osmnx',
        'networkx',
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
    ],
)
