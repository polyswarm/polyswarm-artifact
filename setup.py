from setuptools import setup, find_packages


# The README.md will be used as the content for the PyPi package details page on the Python Package Index.
with open('README.md', 'r') as readme:
    long_description = readme.read()


setup(
    name='polyswarm-artifact',
    version='1.4.2',
    description='Library containing artifact type enums and functions',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='PolySwarm Developers',
    author_email='info@polyswarm.io',
    url='https://github.com/polyswarm/polyswarm-artifact',
    license='MIT',
    python_requires='>=3.6.8',
    install_requires=['pydantic==1.6.1'],
    setup_requires=['pytest-runner'],
    tests_require=[
        'pytest==5.4.1',
        'pytest-runner==5.2',
        'pytest-cov==2.9.0',
        'pytest-asyncio==0.12.0',
        'pytest-timeout==1.3.4',
    ],
    include_package_data=True,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: PyPy',
    ]
)
