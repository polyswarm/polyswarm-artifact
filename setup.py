from setuptools import setup, find_packages


# The README.md will be used as the content for the PyPi package details page on the Python Package Index.
with open('README.md', 'r') as readme:
    long_description = readme.read()


setup(
    name='polyswarm-artifact',
    version='2.0.0',
    description='Library containing artifact type enums and functions',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='PolySwarm Developers',
    author_email='info@polyswarm.io',
    url='https://github.com/polyswarm/polyswarm-artifact',
    license='MIT',
    python_requires='>=3.9',
    install_requires=['pydantic'],
    setup_requires=['pytest-runner'],
    tests_require=[
        'pytest',
        'pytest',
        'pytest-cov',
        'pytest-asyncio',
        'pytest-timeout',
    ],
    include_package_data=True,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: PyPy',
    ]
)
