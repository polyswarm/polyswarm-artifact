from setuptools import setup, find_packages
from src.polyswarmartifact import __version__


def parse_requirements():
    with open('requirements.txt', 'r') as f:
        return [r for r in f.read().splitlines() if not r.startswith('git') and not r.startswith('.')]


# The README.md will be used as the content for the PyPi package details page on the Python Package Index.
with open('README.md', 'r') as readme:
    long_description = readme.read()


setup(
    name='polyswarm-artifact',
    version=__version__,
    description='Library containing artifact type enums and functions',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='PolySwarm Developers',
    author_email='info@polyswarm.io',
    url='https://github.com/polyswarm/polyswarm-artifact',
    license='MIT',
    python_requires='>=3.6.5,<4',
    install_requires=parse_requirements(),
    include_package_data=True,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: PyPy',
    ]
)
