from setuptools import setup, find_packages


version = '0.0.1'

setup(
    name='ws_factorial_service',
    version=version,
    packages=find_packages(),
    install_requires=[
        'aiohttp',
    ],
)
