from os.path import abspath, dirname, join

from setuptools import setup

PROJECT_ROOT = abspath(dirname(__file__))

with open(join(PROJECT_ROOT, 'flake8_strict.py')) as f:
    version_line = [line for line in f if line.startswith('__version__')][0]

__version__ = version_line.split('=')[1].strip().strip("'").strip('"')

readme_path = join(PROJECT_ROOT, 'README.rst')
with open(readme_path) as f:
    long_description = f.read()

setup_arguments = dict(
    name='flake8_strict',
    version=__version__,
    description='Flake8 plugin that checks Python code against '
    'a set of opinionated style rules',
    long_description=long_description,
    url='https://github.com/smarkets/flake8-strict',
    author='Smarkets Limited',
    author_email='support@smarkets.com',
    maintainer='Smarkets Limited',
    maintainer_email='support@smarkets.com',
    keywords=[
        'flake8',
        'plugin',
        'strict',
        'hanging indent',
        'trailing comma',
        'trailing commas',
    ],
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Quality Assurance',
    ],
    py_modules=['flake8_strict'],
    install_requires=[
        'enum-compat',
        'flake8',
        'setuptools',
    ],
    entry_points={
        'flake8.extension': [
            'S = flake8_strict:Flake8Checker',
        ],
    },
    zip_safe=False,
)

if __name__ == '__main__':
    setup(**setup_arguments)
