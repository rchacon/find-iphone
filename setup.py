import os
from setuptools import setup


def get_version():
    with open(os.path.join('apple', '__init__.py')) as f:
        for line in f:
            if line.startswith('__version__'):
                return eval(line.split('=')[-1])


def get_long_description():
    descr = []
    with open('README.md') as f:
        descr.append(f.read())
    return '\n\n'.join(descr)


setup(
    name='find-iphone',
    version=get_version(),
    description="Command line tool for finding your iPhone",
    long_description=get_long_description(),
    keywords='apple iphone icloud',
    author='Raul J. Chacon',
    url='https://github.com/rchacon/find-iphone',
    license='MIT license',
    packages=['apple'],
    package_dir={'apple': 'apple'},
    include_package_data=True,
    install_requires=[
        'lxml==4.6.2',
        'requests==2.22.0'
    ],
    entry_points={
        'console_scripts': [
            'find-iphone = apple.cli:main',
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License"
    ],
)
