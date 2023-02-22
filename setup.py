from setuptools import setup, find_packages

VERSION = '0.0.0'
DESCRIPTION = 'Quantifies certain evironmental factors that affect cycling'
LONG_DESCRIPTION = """
This package is intended to be used by researchers to quantify some environmental factors that affect cycling for a given region.
"""


setup(
    name='bikenv',
    packages=find_packages(include=['bikenv']),
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author='Fabián Abarca',
    license='MIT',
    install_requires=[
        'numpy',
        'scipy',
        'pandas',
        'requests',
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
    ],
)
